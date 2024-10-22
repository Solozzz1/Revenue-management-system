// Custom JavaScript for additional interactivity
$(document).ready(function() {
    // You can add custom JavaScript or jQuery logic here
    console.log("Page loaded successfully");
    
    // Example: Smooth scroll for navigation links
    $('a.nav-link').on('click', function(event) {
        event.preventDefault();
        var target = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(target).offset().top
        }, 1000);
    });
});
