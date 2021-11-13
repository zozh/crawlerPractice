function render(node, splits) {

    splits.tag += '|----';
    console.log(splits.tag + node.tagName);

    var children = node.children;
    if (!children) return;
    for (var i = 0, len = children.length; i < len; i++) {
        var child = children[i];
        var _tag = splits.tag;
        render(child, splits);
        splits.tag = _tag;
    }
}
var splits = { tag: '' }
var start = (new Date()).getTime();
render(document.body, splits);
var end = (new Date()).getTime();
console.log('Cost: ' + (end - start) + 'ms');
var splits = { tag: '' }
var start = (new Date()).getTime();
render(document.body, splits);
var end = (new Date()).getTime();
console.log('Cost: ' + (end - start) + 'ms');