API endpoints:

GET/POST  http://<server>:5000/isAlive -> 'server is alive, <request type> recived'

POST  http://<server>:5000/blur-dir -> 

POST  http://<server>:5000/blur-test-local -> 


Runung on an aws g5 instace:
 
install nvidia driver version: 470.xxx checked using (470.239.06)

To install NVIDIA driver version 470.239.06 on an Ubuntu 22.04 SSH client server, follow these steps:

1. Update your system:
   ```
   sudo apt update && sudo apt upgrade -y
   ```

2. Install required packages:
   ```
   sudo apt install build-essential gcc-multilib dkms
   ```

3. Remove any existing NVIDIA drivers:
   ```
   sudo apt-get purge nvidia*
   ```

4. Add the NVIDIA driver PPA:
   ```
   sudo add-apt-repository ppa:graphics-drivers/ppa
   sudo apt update
   ```

5. Install the specific driver version:
   ```
   sudo apt install nvidia-driver-470
   ```
   Note: The package name might not exactly match the version number 470.239.06, but it will install the latest 470.xx driver.

6. Reboot your system:
   ```
   sudo reboot
   ```

7. After reboot, verify the installation:
   ```
   nvidia-smi
   ```


should output
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.239.06   Driver Version: 470.239.06   CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA A10G         Off  | 00000000:00:1E.0 Off |                    0 |
|  0%   29C    P0    52W / 300W |      0MiB / 22731MiB |      5%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+


I apologize for the confusion. You're right, you specifically asked for NVIDIA Docker 2. Here's the process to install NVIDIA Docker 2 on Ubuntu 22.04:

1. Update your system:
   ```
   sudo apt update && sudo apt upgrade -y
   ```

2. Install necessary packages:
   ```
   sudo apt install curl apt-transport-https ca-certificates software-properties-common
   ```

3. Install NVIDIA drivers (if not already installed):
   ```
   sudo apt install nvidia-driver-470
   ```
   (Adjust the driver version if needed)

4. Reboot your system:
   ```
   sudo reboot
   ```

5. Install Docker (if not already installed):
   ```
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

6. Add your user to the Docker group:
   ```
   sudo usermod -aG docker $USER
   ```
   (Log out and back in for this to take effect)

7. Install NVIDIA Docker 2:
   ```
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

   sudo apt-get update
   sudo apt-get install -y nvidia-docker2
   ```

8. Configure Docker daemon:
   ```
   sudo tee /etc/docker/daemon.json <<EOF
   {
       "default-runtime": "nvidia",
       "runtimes": {
           "nvidia": {
               "path": "nvidia-container-runtime",
               "runtimeArgs": []
           }
       }
   }
   EOF
   ```

9. Restart Docker:
   ```
   sudo systemctl restart docker
   ```

10. Verify the installation:
    ```
    sudo docker run --gpus all --rm nvidia/cuda:11.0-base nvidia-smi
    ```
    This should display information about your GPU.

11. Run TensorFlow with GPU support:
    ```
    sudo docker run --runtime=nvidia -it tensorflow/tensorflow:2.16.1-gpu
    ```

12. Inside the TensorFlow container, you can verify GPU access:
    ```python
    import tensorflow as tf
    print(tf.config.list_physical_devices('GPU'))
    ```

This process installs NVIDIA Docker 2 and configures it to be the default runtime for Docker. Note that while this method still works, it's considered legacy. The `--runtime=nvidia` flag is used instead of `--gpus all`.

If you encounter any issues during this process, please let me know, and I'll be happy to help you troubleshoot.


runing on the instance
docker run --gpus all -p 5000:5000 --restart unless-stopped -v /path/to/host/directory:/path/to/container/directory anonyfacejsonresp
