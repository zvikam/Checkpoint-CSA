#!/bin/bash

#for ff in *.pptx; do mkdir ${ff%%.*}; pushd ${ff%%.*}; unzip -qc "../${ff}" ppt/slides/slide*.xml | grep -oP '(?<=\<a:t\>).*?(?=\</a:t\>)' > text; popd; done

_SOLUTION=

_getNextLine() {
    cat $1/text | head -$2 | tail -1
}

_nextStep() {
    IFS=', '; arrIN=($@); unset IFS;
    local _nextCHAR=${arrIN[0]}
    local _nextFILE=${arrIN[2]}
    local _nextLINE=${arrIN[4]}
    _SOLUTION="${_SOLUTION}${_nextCHAR}"
    if [[ -f "${_nextFILE}" ]]; then
        _nextStep $(_getNextLine ${_nextFILE%%.*} ${_nextLINE})
    fi
}

_nextStep `_getNextLine START 1`
echo ${_SOLUTION}
