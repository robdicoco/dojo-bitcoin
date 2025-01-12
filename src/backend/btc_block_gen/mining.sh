# mining.sh
#!/bin/bash

echo "Generating a block every 15 minutes. Press [CTRL+C] to stop..."

address="bcrt1qm46a66rjckz6yh4t0qy5k036p0wrn5qktdg0mk"

while :
do
        echo "Generate a new block `date '+%d/%m/%Y %H:%M:%S'`"
        bitcoin-cli generatetoaddress 1 $address
        sleep 900
done