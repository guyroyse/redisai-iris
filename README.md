# Iris Classification with RedisAI

## Step 0: Setup RedisAI

To use RedisAI, well, you need RedisAI. I've found the easiest way to do this is with Docker. First, pull the redismod image—it contians Redis with several popular modules ready to go:

    $ docker image pull redislabs/redismod

Then run the image:

    $ docker run \
        -p 6379:6379 \
        redislabs/redismod \
        --loadmodule /usr/lib/redis/modules/redisai.so \
          ONNX redisai_onnxruntime/redisai_onnxruntime.so

And, you've got RedisAI up and running!

## Step 1: Setup Python Environment

You need a Python environment to make this all work. I used Python 3.8—the latest, greatest, and most updatest at the time of this writing. I also used `venv` to manage my environment.

I'll assume you can download and install Python 3.8 on your own. So lets go ahead and setup the environment:

    $ python3.8 -m venv venv

Once `venv` is installed, you need to activate it:

    $ . venv/bin/activate

Now when you run `python` from the command line, it will always point to Python3.8 and any libraries you install will only be for this specific environment. Usually, this includes a dated version of pip so go ahead an update that as well:

    $ pip install --upgrade pip


If you want to deactivate this environment, you can do so from anywhere with the following command:

    $ deactivate

## Step 2: Install Dependencies

Next, let's install all the dependencies. These are all listed in `requirements.txt` and can be installed with `pip` like this.

    $ pip install -r requirements.txt

Run that command, and you'll have all the dependencies installed and will be ready to run the code.

## Step 3: Build the ONNX Model

This is as easy as running the following:

    $ python build.py

## Step 4: Deploy the Model into RedisAI

NOTE: This requires tge redis-cli. If you don't have redis-cli, I've found the easiest way to get it is to download, build, and install Redis itself. Details can be found at the [Redis quickstart](https://redis.io/topics/quickstart) page:

    $ redis-cli -x AI.MODELSET iris ONNX CPU BLOB < log_reg_iris.onnx

## Step 5: Make Some Predictions

Launch redis-cli:

    $ redis-cli

Set the input tensor with 2 sets of inputs of 4 values each:

    > AI.TENSORSET iris_in FLOAT 2 4 VALUES 5.0 3.4 1.6 0.4 6.0 2.2 5.0 1.5

Make the predictions:

    > AI.MODELRUN iris INPUTS iris_in OUTPUTS iris_out:predictions iris_out:scores

Check the predictions:

    > AI.TENSORGET iris_out:predictions VALUES

    1) (integer) 0
    2) (integer) 2

Check the scores:

    > AI.TENSORGET iris_out:scores VALUES

    (error) ERR tensor key is empty

What? The output tensor for the scores is required to run the model, but nothing is written to it. I'm still trying to track down this bug. `¯\_(ツ)_/¯`
