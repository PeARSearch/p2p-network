# p2p-network
The P2P network for PeARS



## Setup PeARS by checking out to the indexer branch

Make sure you install all requirements from requirements.txt and that
you have openvectors.db populated using the script uncompress_db

Build the pear profile using the code browser_history_indexer.py

`python browser_history_indexer.py`


## Run the DHT

Clone the p2p-network code from the master branch

Start the DHT by running the following:

`python dht.py 4000`

This runs a standalone DHT node in your local machine in the port 4000.
If you know the IP of another node that has a DHT running, then you can
do the following to make the nodes identify each other:

`python dht.py 4000 <Known node IP> <Known node port>`


## Try searching from your local history

Once the above steps are done, open up your browser and go to
locahost:5000. Do try to search for something from your local index and
hope for the best. :-)


## Notes

The issues that need loving:

1. There is no way of telling the indexer what to index now. We end up
   getting a lot of pages like mail home etc. indexed which is not relevant. I have to fix this.
2. The DHT hashing is not really efficient. It randomly picks buckets,
   although there is a hash function that picks the node.
3. A lot of testing to do. I haven't yet tested DHT across several
   machines. I tested it all using docker and all the containers
communicated using internal IP. I am not even sure if it works properly
if DHT setup across different nodes are connected.


