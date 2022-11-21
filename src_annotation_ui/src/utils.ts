function getIndicies(needle: string, hay: string, caseSensitive) {
    var searchStrLen = needle.length;
    if (searchStrLen == 0) {
        return [];
    }
    var startIndex = 0, index, indices = [];
    if (!caseSensitive) {
        hay = hay.toLowerCase();
        needle = needle.toLowerCase();
    }
    while ((index = hay.indexOf(needle, startIndex)) > -1) {
        indices.push(index);
        startIndex = index + searchStrLen;
    }
    return indices;
}

export {getIndicies}