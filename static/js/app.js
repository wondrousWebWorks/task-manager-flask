document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {
        edge: 'right'
    });

    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems);
});
