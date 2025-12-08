# Real Time AASX

## About the Project

This project was made for the ICT Trends class to research the robot Ned 2.
This project includes a Web UI Server, an OPC UA Server, and an OPC UA Client.

The Web UI server displays an AAS file, the OPC UA Client modifies the AAS file from an CSV file, and the OPC UA Server updates the AAS file.

The project was developed on Linux systems.

## Getting Started

### Prerequites

This project requires Docker Desktop, XQuartz, and Python 3.10.9.

* [![Docker](https://img.shields.io/badge/Docker_Download-2496ED?style=for-the-badge&logo=docker&logoColor=fff)](https://www.docker.com/)
* [![XQuartz][XQuartz.org]](https://www.xquartz.org/)
* [![Python](https://img.shields.io/badge/Python_Download%20-3776AB?style=for-the-badge&logo=python&logoColor=fff)](https://www.python.org/downloads/)

### Docker Setup

After downloading Docker Desktop, create the following images and volume. Make sure XQuartz is open and running in the background.

1. Create the shared volume in the Terminal.

```bash
docker volume create shared_aasx
```

2. You can put your .aasx files in /aasx_files. Make a copy of your .aasx file and rename it `Updated_Your_Robot.aasx`
   Make sure to change the file names in `OpcUaServer.py` if you do this.

```python
# Path inside container
aasx_path = "/aasx_files/original/Your_Robot.aasx"
updated_aasx_path = "/aasx_files/Updated_Your_Robot.aasx"
```
   

3. Add the local files to the shared volume. 

```bash
docker run --rm \
  -v shared_aasx:/tmp_data \
  -v /Users/your_username/file_path_to/aasx_files:/tmp_local \
  busybox \
  sh -c "mkdir -p /tmp_data/original" \
  sh -c "cp /tmp_local/Your_Robot.aasx /tmp_data/original" \
  sh -c "cp /tmp_local/Updated_Your_Robot.aasx /tmp_data"
```

4. Create and run the Web UI Server. This command will create the image and container, and run the server. You can view the Web UI at `http://localhost:5001`.

```bash
docker run --rm -it \
  --name web_ui_server \
  -p 5001:5001 \
  -v shared_aasx:/AasxServerBlazor/aasxs \
  adminshellio/aasx-server-blazor-for-demo:main \
  --external-blazor http://localhost:5001 \
  --load /AasxServerBlazor/aasxs/Updated_Your_Robot.aasx
```

### OPC UA Server and Client Setup

1. Clone the repository from GitHub.

```bash
git clone https://github.com/msroque/RealTimeAasx.git
```

2. In a separate Terminal, navigate to where you saved the project. Build the OPC UA Server.
   If you are asked to allow access to other apps, allow so that the terminal can access Docker Desktop.

```bash
cd server
docker build -t opcua-server .
```

3. Run the OPC UA Server.

```bash
docker run --rm -p 4840:4840 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v shared_aasx:/aasx_files \
  opcua-server
```

4. In a separate Terminal, run the OPC UA Client.

```bash
cd client
python3 OpcUaClient.py
```

## Usage
1. Open `http://localhost:5001` on your browser to view the .aasx file. You will have to refresh the page when the server is reloaded.
2. Have the Terminals for the server and client next to each other so that you can see the changes on both at the same time.
3. Follow the prompts on the client terminal, and watch the changes happen on the servers.

### Server and Client - Terminals at Start Up

<img src="pics/startup.png" alt="Terminals at Startup">

### Server and Client - Terminals at Update

<img src="pics/update.png" alt="Terminals at Startup">

## Retrieving Updated AASX File

To end the Terminal intructions, press `Ctrl + C`.
If you want to download the new updated .aasx file, you can download it from the shared volume on Docker Desktop, or you can run the following command.

```bash
docker run --rm \
  -v shared_aasx:/tmp_data \
  -v /Users/your_username/file_path_to/aasx_files:/tmp_local \
  busybox \
  sh -c "cp /tmp_data/Updated_Your_Robot.aasx /tmp_local/Updated_Your_Robot.aasx"
```

[XQuartz.org]: https://img.shields.io/badge/XQuartz_Download-2496ED?style=for-the-badge&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/Pgo8IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDIwMDEwOTA0Ly9FTiIKICJodHRwOi8vd3d3LnczLm9yZy9UUi8yMDAxL1JFQy1TVkctMjAwMTA5MDQvRFREL3N2ZzEwLmR0ZCI+CjxzdmcgdmVyc2lvbj0iMS4wIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiB3aWR0aD0iMTEyLjAwMDAwMHB0IiBoZWlnaHQ9Ijk4LjAwMDAwMHB0IiB2aWV3Qm94PSIwIDAgMTEyLjAwMDAwMCA5OC4wMDAwMDAiCiBwcmVzZXJ2ZUFzcGVjdFJhdGlvPSJ4TWlkWU1pZCBtZWV0Ij4KCjxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAuMDAwMDAwLDk4LjAwMDAwMCkgc2NhbGUoMC4xMDAwMDAsLTAuMTAwMDAwKSIKZmlsbD0iI2ZmZiIgc3Ryb2tlPSJub25lIj4KPHBhdGggZD0iTTEyMCA5NTggYzAgLTcgMzIgLTU2IDcwIC0xMDggMzkgLTUyIDcwIC05NyA3MCAtMTAwIDAgLTMgLTIxIC0xNwotNDggLTMyIC0xMjYgLTcxIC0xOTIgLTE3MCAtMTkyIC0yODggMCAtODggMzIgLTE1MiAxMTEgLTIyMyBsNTkgLTU0IC0zNSAtNDYKYy0xOSAtMjUgLTM1IC00OCAtMzUgLTUxIDAgLTMgMjIgLTYgNDkgLTYgNDQgMCA1MSAzIDcxIDMzIGwyMiAzMyA3MiAtMjYgYzY1Ci0yMyA4NSAtMjUgMjQ4IC0yNiA5OCAwIDE4MSAtMyAxODQgLTcgMTAgLTEwIDI0NCAtOSAyNDQgMSAtMSA0IC0xNCAyMyAtMzAKNDIgLTE3IDE5IC0zMCAzOSAtMzAgNDUgMCA1IDI1IDMxIDU0IDU3IDE3OSAxNTcgMTM0IDM5NyAtOTcgNTE5IC0zNCAxNyAtNjQKMzMgLTY2IDM1IC0yIDIgMjkgNDUgNjkgOTYgNDAgNTEgNzcgOTkgODMgMTA2IDcgOSAtMyAxMiAtNDUgMTIgbC01NSAwIC03MgotOTQgLTcxIC05NCAtMzggOSBjLTIwIDUgLTgxIDkgLTEzNCA5IGwtOTcgMCAtNTkgODMgLTU4IDgyIC0xMjIgMyBjLTk0IDIKLTEyMiAwIC0xMjIgLTEweiBtNTg3IC0yMjEgYzIgLTMgLTE3IC0zMyAtNDMgLTY2IC0yNiAtMzQgLTUwIC01OCAtNTQgLTU0IC00CjUgLTIzIDMyIC00NCA2MiAtMzAgNDIgLTM1IDU2IC0yNCA2MyAxMyA5IDE1NSA0IDE2NSAtNXogbTE1NCAtNDggYzU1IC0yOAoxMjYgLTk1IDE1MCAtMTQwIDQ0IC04NyAzMyAtMTY5IC0zNCAtMjUxIC03OSAtOTYgLTY5IC05OSAtMTg5IDY5IC01NyA4MQotMTA4IDE1NCAtMTEyIDE2MSAtOSAxNiAxMTUgMTgyIDEzNiAxODIgNSAwIDI3IC05IDQ5IC0yMXogbS01MTQgLTU2IGMxNiAtMjEKNDYgLTYxIDY2IC04OSBsMzcgLTUxIC04NSAtMTExIGMtNDcgLTYxIC05MSAtMTE0IC05NyAtMTE4IC03IC01IC0yNyA5IC00OAozNCAtODkgMTAwIC03NSAyMzMgMzUgMzMwIDI2IDIzIDUxIDQyIDU2IDQyIDQgMCAyMCAtMTcgMzYgLTM3eiBtMjU1IC0zNDcKYzg4IC0xMjMgOTQgLTEzNSA3NSAtMTQwIC02NCAtMTcgLTIyNSA0IC0zMDYgNDEgbC00MCAxOCA4MiAxMDcgYzQ1IDYwIDg0CjEwOCA4NyAxMDggMyAtMSA0OCAtNjEgMTAyIC0xMzR6Ii8+CjwvZz4KPC9zdmc+Cg==
