#!/bin/bash

for UTIL in scripts/*.py; do
    BUTIL=`basename $UTIL .py`
    cat << EOF > bin/$BUTIL
#!/bin/bash

module add alphafold-conda

python \$AF_TOOLS/scripts/${BUTIL}.py "\$@"
EOF
chmod 755 bin/$BUTIL
done
