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

// Open Tweet detail page
function openDetailTweet(tweetUrl) {
    window.location.href = tweetUrl
}

// call like rest api
function likeTweet(likeUrl){
    likeUrl = likeUrl + "like/"

    $.ajax({
        url: likeUrl,
        method: 'GET',
        data: {},
        success: function(data) {
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

function getUsersWhoLiked(likeUrl) {
    likeUrl = likeUrl + "like/users/"

    $.ajax({
        url: likeUrl,
        method: 'GET',
        data: {},
        success: function(data) {
            console.log(data)
            $(".modal-title")[0].innerText = "Liked by"

            bodyStr = "<ul class='list-group list-group-flush'>"
            for(var i in data){
                username = data[i]
                userUrl = "user/" + username
                // bodyStr = bodyStr + "<div><a href='"+ userUrl + "'>" + username +"</a></div>\n"
                bodyStr = bodyStr + "<li class='list-group-item'><a href='"+ userUrl + "'>" + username +"</a></li>\n"
            }
            $(".modal-body")[0].innerHTML = bodyStr + "</ul>"
        },
        error: function(error){
            console.log(error)
        }
    })
}

// function comment_on_tweet(tweetUrl) {
//     tweetUrl = tweetUrl + "comment/"
//     body = $("#commentBox")[0].innerText

//     $.ajax({
//         url: tweetUrl,
//         method: 'POST',
//         data: {'body': body},
//         beforeSend: function(xhr) {
//             xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
//           },
//         success: function(data) {
//             console.log(data)
//         },
//         error: function(error){
//             console.log(error)
//         }
//     })
// }

function deleteComment(commentUrl, commentId){
    $.ajax({
        url: commentUrl,
        method: 'GET',
        data: {},
        success: function(data) {
            console.log(data)
            commentId = "#comment-" + commentId
            
            // Show toast
            $(".toast-header")[0].innerText = "Delete"
            $(".toast-body")[0].innerText = "Comment successfully deleted"
            $('.toast').toast('show');

            // Remove element from screen
            $(commentId).remove()

            // Update number of comments
            commentCountId = "#commentCount-" + data.tweet_id
            $(commentCountId)[0].innerText = data.comments_on_tweet + " comments"
        },
        error: function(error){
            console.log(error)
        }
    })
}