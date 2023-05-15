$(document).ready(function () {

    // Loop through buttons of left pane of accounts page and add a mouseover
    // event listener to each one.
    Array.from(document.getElementsByClassName("menu-button")).forEach(function(item) {
        item.addEventListener('mouseover', () => {
            if(!item.classList.contains('hover-btn')) {
                item.classList.add('hover-btn');
                $(item).find('*').addClass('hover-btn');
            }
        });
    });
    
    // Loop through buttons of left pane of accounts page and add a mouseout
    // event listener to each one so the button reverts back to its original
    // colours once the user has moved their mouse off the button.
    Array.from(document.getElementsByClassName("menu-button")).forEach(function(item) {
        item.addEventListener('mouseout', () => {
            item.classList.remove('hover-btn');
            $(item).find('*').removeClass('hover-btn');
        });
    });

    // Loop through buttons of left pane of accounts page and add a click
    // event listener to each one so that the button's colours invert and remain
    // that way when the user clicks on it. Linked to usability requirement about
    // user receiving feedback.
    Array.from(document.getElementsByClassName("menu-button")).forEach(function(item) {
        item.addEventListener('click', () => {
            Array.from(document.getElementsByClassName("menu-button")).forEach(function(i) {
                if(i.classList.contains('current')) {
                    i.classList.remove('current');
                    $(i).find('*').removeClass('current');
                }
            });
            item.classList.add('current');
            $(item).find('*').addClass('current');
        });
    });
});
