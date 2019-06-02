internal_ip1 = $1 
internal_ip2 = $2 
sudo apt-get install mpich
echo $internal_ip1 >> hosts
echo $internal_ip2 >> hosts
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo pip install mpi4py
sudo apt-get install python3-dev
sudo apt-get install python3-pip
sudo pip3 install mpi4py
sudo pip3 install numpy
sudo pip3 install numpy
sudo pip3 install scipy 

