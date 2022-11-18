#!/usr/bin/bash

cd data_bigrets

# https://cs.pomona.edu/~dkauchak/simplification/
wget -nc https://cs.pomona.edu/~dkauchak/simplification/data.v2/sentence-aligned.v2.tar.gz
tar -xvzf sentence-aligned.v2.tar.gz

wget -nc https://cs.pomona.edu/~dkauchak/simplification/human_simplification.data.zip
unzip human_simplification.data.zip

# https://github.com/tmu-nlp/sscorpus/blob/master/sscorpus.gz
# TODO: this is outdated and we may do better
wget -nc https://github.com/tmu-nlp/sscorpus/raw/master/sscorpus.gz
gzip -d sscorpus.gz

# onestopenglish
# TODO

# minwiki
wget -nc https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_train.complex
wget -nc https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_train.simple
wget -nc https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_test.complex
wget -nc https://raw.githubusercontent.com/serenayj/DeSSE/main/MinWiki/matchvp_test.simple

cd ../