#!/usr/bin/env bash

for i in {1..150}
do
    cp Archivos/ArchivoCliente/Daft_Punk_One_More_Time.mp3 /nfs/Archivos/ArchivoCliente/Daft_Punk_One_More_Time_$i.mp3

    echo ../Archivos/ArchivoCliente/Daft_Punk_One_More_Time_$i.mp3,.wav >> JmeterTest/tareasMasivo.cvs
done
