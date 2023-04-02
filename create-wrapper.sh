#!/bin/bash

for UTIL in scripts/*.py; do
    BUTIL=`basename $UTIL .py`
    cat << EOF > bin/$BUTIL
#!/bin/bash

module add alphafold-conda

# fix problems with:
# qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
export QT_QPA_PLATFORM=offscreen

python \$AF_TOOLS/scripts/${BUTIL}.py "\$@"
EOF
chmod 755 bin/$BUTIL
done
