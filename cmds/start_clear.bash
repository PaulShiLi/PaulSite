# Kill all python processes via netstat

# Iterate 2 times to make sure all processes are killed

for i in {1..2}
do
    # Get PID of python processes
    PID=$(netstat -tulpen | grep python | awk '{print $9}' | awk -F '/' '{print $1}')

    # Check if PID is empty
    if [ -z "$PID" ]
    then
        echo "No python processes running"
        break
    else
        echo "Killing python processes"
        kill -9 $PID
    fi
done
