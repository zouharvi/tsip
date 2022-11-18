#!/usr/bin/bash

mkdir -p data

wget -P data/ https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_train.complex
wget -P data/ https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_train.simple
wget -P data/ https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_test.complex
wget -P data/ https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_test.simple