import zipfile
from opcua import Server
from basyx.aas.adapter import aasx
from basyx.aas.model import Property
from basyx.aas.model.provider import DictObjectStore
import time
import docker

# Path inside container is from shared volume
aasx_path = "/aasx_files/original/Niryo-RobotAsset.aasx"
updated_aasx_path = "/aasx_files/Updated-Niryo-RobotAsset.aasx"

# Get Web UI Server Container
dockerClient = docker.from_env()
container = dockerClient.containers.get("web_ui_server")

# Stores for AAS objects
objects = DictObjectStore()
files = aasx.DictSupplementaryFileContainer() 

# Read the AASX
with aasx.AASXReader(updated_aasx_path) as reader:
    meta_data = reader.get_core_properties()
    reader.read_into(objects, files)

# Setup OPC UA Server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840")
idx = server.register_namespace("http://example.org/aasx")
objects_node = server.get_objects_node()

# Submodel: OperationalData
aas = objects.get_identifiable('https://idta.org/ids/sm/0433_9050_2152_5753')
submodel_node = objects_node.add_object(idx, aas.id_short)

ua_nodes = {}

for elem in aas.submodel_element:
    if isinstance(elem, Property):
        # Create a writable variable node for each property
        ua_node = submodel_node.add_variable(
            idx,
            elem.id_short,
            elem.value
        )
        ua_node.set_writable()  # allow client write

        # Save reference for updating loop
        ua_nodes[elem.id_short] = ua_node

        print(f"{elem.id_short} = {elem.value}")


server.start()
print("OPC UA server started at opc.tcp://0.0.0.0:4840")

try:
    while True:
        updated = False

        for elem in aas.submodel_element:
            if isinstance(elem, Property):

                # Get OPC UA node
                node = ua_nodes[elem.id_short]
                value = node.get_value()

                # Update node if needed
                if elem.value != value:
                    print(f"Updating AAS Properties...", flush=True)
                    updated = True
                    elem.value = value

                    # Write to the AASX
                    with aasx.AASXWriter(updated_aasx_path) as writer:
                        writer.write_aas("https://idta.org/ids/aas/0551_9050_2152_6239",
                            objects,
                            files
                        )
                        writer.write_core_properties(meta_data)

                print(f"{elem.id_short}: {elem.value}", flush=True)

        # Reload Web UI Server with updated .aasx file
        if updated == True:
            # restart Web UI
            container.restart()
            print("Web UI Reload Triggered.")
            updated = False

        time.sleep(0.5)
finally:
    server.stop()

