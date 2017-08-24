dir=$1
data=$2
cd $dir
cd data
ln -s $data"/AICdevkit" AICdevkit
cd ..
git clone https://github.com/Microsoft/caffe.git
cd lib
make
cd ../caffe
git reset --hard 1a2be8e
cp ../tools/Makefile.config .
cp ../tools/Makefile .
make -j8 && make pycaffe
