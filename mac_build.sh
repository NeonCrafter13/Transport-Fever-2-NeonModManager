pushd ./src || exit
python ./package.py bdist_mac || true
codesign -f -s willwill2will@gmail.com --deep ./build/*.app || true
popd || exit