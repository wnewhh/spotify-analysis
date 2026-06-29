#!/bin/bash
USER_NAME="wne"
HDFS_INPUT_DIR="/user/$USER_NAME/input"
LOCAL_FILE="data/spotify.csv"

hdfs dfs -mkdir -p $HDFS_INPUT_DIR
hdfs dfs -put -f $LOCAL_FILE $HDFS_INPUT_DIR/
hdfs dfs -ls $HDFS_INPUT_DIR/