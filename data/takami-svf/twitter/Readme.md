#!/bin/sh

sed '/ *label.*/d' 4dai_uni_d.gml > 4dai_uni_d_nolabel.gml
cp 4dai_uni_d.labels 4dai_uni_d_nolabel.labels

sed '/ *label.*/d' techchan_uni_d.gml > techchan_uni_d_nolabel.gml
cp techchan_uni_d.labels techchan_uni_d_nolabel.labels
