// Used to toggle the menu on smaller screens when clicking on the menu button
function openNav() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
}

// Infinite scrolling
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    // handler: function(direction) {},
    offset: 'bottom-in-view',

    onBeforePageLoad: function () {
        $('.spinner-border').show();
    },
    onAfterPageLoad: function () {
        $('.spinner-border').hide();
    }
});

// Accordion
function myFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += " w3-theme-d1";
    } else { 
        x.className = x.className.replace("w3-show", "");
        x.previousElementSibling.className = 
        x.previousElementSibling.className.replace(" w3-theme-d1", "");
    }
}
  
// Create Tweet Page
function openCreateTweet() {
    window.location.href = "{% url 'tweet-create' %}"
}

// Open Tweet detail page
function openDetailTweet(tweetUrl) {
    window.location.href = tweetUrl
}

// call like rest api
function likeTweet(likeUrl){
    likeUrl = likeUrl + "/like/"

    $.ajax({
        url: likeUrl,
        method: 'GET',
        data: {},
        success: function(data) {
        console.log(data)
        likeCountId = "#likeCount-" + data.id
        $(likeCountId)[0].innerText = data.count + " likes"

        likeButtonId = "#likeButton-" + data.id
        if (data.like){
            $(likeButtonId)[0].innerHTML = '<i class="fa fa-thumbs-down"></i> &nbsp;Unlike'
        }
        else {
            $(likeButtonId)[0].innerHTML = '<i class="fa fa-thumbs-up"></i> &nbsp;Like'
        }
        
        },
        error: function(error){
            console.log(error)
        }
    })
}