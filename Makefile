ads1256.so: ads1256_test.c wrapper.c 
	python setup.py build_ext --inplace
	echo "\n Para testar a lib execute:\n python test.py";

