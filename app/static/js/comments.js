function comment(postUrl, slug, userName, firstName, lastName) {
    var text = "";
    $('.comment-submit').click(function () {
        text = $('.comment-field').val();
        var data = {
            slug: slug,
            text: text,
            username: userName,
            firstname: firstName,
            lastname: lastName
        };
        $.post(postUrl, data).done(function (data) {
            addComment("commenting", data.id, text, userName, firstName, lastName, data.date);

        }).fail(function () {
            alert("Something went wrong. Please try again!");
        });
    });

}
function commentReply(postUrl, slug, userName, firstName, lastName) {
    $('.comments').on('click', '.comment-reply', function () {
        var comment_id = $(this)[0].id.split('-')[3];
        $('#comment-' + comment_id).append(commentDIV(comment_id));
        $('#field-' + comment_id).focus();
        $('#reply-to-comment-' + comment_id).remove();
    });

    $('body').on('click', '.comment-reply-submit', function () {
        var commentId = $(this)[0].className.split(' ')[0].split('-')[2];
        var text = $('.comment-of-' + commentId).val();
        var data = {
            slug: slug,
            reply_of: commentId,
            text: text,
            username: userName,
            firstname: firstName,
            lastname: lastName
        };
        $.post(postUrl, data).done(function (data) {

            addCommentReply("commenting", commentId, data.id, text, userName, firstName, lastName, data.date);

            $('html,body').animate({
                scrollTop: $('#comment-' + data.id).offset().top - 100
            });
            $('#comment-' + data.id).effect('highlight', {}, 3000);
            $('comment-of-' + data.id).val('');

        }).fail(function () {
            alert("Something went wrong. Please try again!");
        });
        $('.reply-comment-field').val('');
    });

}
function commentDIV(id) {
    div = '<div id="field-' + id + '" class="row">' +
        '<div class="col-md-7 col-md-offset-2 col-xs-8 col-xs-offset-2">' +
        '<textarea class="reply-comment-field comment-of-' + id + '"></textarea>' +
        '</div>' +
        '</div>' +
        '<div class="col-md-3 col-md-offset-6 col-sm-4 col-sm-offset-4 col-xs-6 col-xs-offset-4 text-right">' +
        '<button class="reply-to-' + id + ' comment-reply-submit btn btn-reply ">Reply</button>' +
        '</div>' +
        '</div>';
    return div;
}
function getComments(post_url, slug) {
    var comments = $.post(post_url, {slug: slug}).done(function (data) {
        var comments_data = JSON.parse(data);
        for (var i in comments_data) {
            if (comments_data[i]['reply_of'] != undefined) {
                addCommentReply("listing", comments_data[i]['reply_of']['$oid'], comments_data[i]['_id']['$oid'], comments_data[i]['text'], comments_data[i]['username'], comments_data[i]['firstname'], comments_data[i]['lastname'], comments_data[i]['date'], comments_data[i]['avatar_url']);
            } else {
                addComment("listing", comments_data[i]['_id']['$oid'], comments_data[i]['text'], comments_data[i]['username'], comments_data[i]['firstname'], comments_data[i]['lastname'], comments_data[i]['date'], comments_data[i]['avatar_url']);
            }
        }
    }).fail(function () {
        alert("Something went wrong. Please try again!");
    });

}

function time_ago(time) {
    if (time != undefined) {
        time = new Date(time['$date'])
    }else{
        time = new Date();
    }

    switch (typeof time) {
        case 'number':
            break;
        case 'string':
            time = +new Date();
            break;
        case 'object':
            if (time.constructor === Date) time = time.getTime();
            break;
        default:
            time = +new Date();
    }
    var time_formats = [
        [60, 'seconds', 1], // 60
        [120, '1 minute ago', '1 minute from now'], // 60*2
        [3600, 'minutes', 60], // 60*60, 60
        [7200, '1 hour ago', '1 hour from now'], // 60*60*2
        [86400, 'hours', 3600], // 60*60*24, 60*60
        [172800, 'Yesterday', 'Tomorrow'], // 60*60*24*2
        [604800, 'days', 86400], // 60*60*24*7, 60*60*24
        [1209600, 'Last week', 'Next week'], // 60*60*24*7*4*2
        [2419200, 'weeks', 604800], // 60*60*24*7*4, 60*60*24*7
        [4838400, 'Last month', 'Next month'], // 60*60*24*7*4*2
        [29030400, 'months', 2419200], // 60*60*24*7*4*12, 60*60*24*7*4
        [58060800, 'Last year', 'Next year'], // 60*60*24*7*4*12*2
        [2903040000, 'years', 29030400], // 60*60*24*7*4*12*100, 60*60*24*7*4*12
        [5806080000, 'Last century', 'Next century'], // 60*60*24*7*4*12*100*2
        [58060800000, 'centuries', 2903040000] // 60*60*24*7*4*12*100*20, 60*60*24*7*4*12*100
    ];
    var seconds = (+new Date() - time) / 1000,
        token = 'ago', list_choice = 1;

    if (seconds == 0) {
        return 'Just now'
    }
    if (seconds < 0) {
        seconds = Math.abs(seconds);
        token = 'from now';
        list_choice = 2;
    }
    var i = 0, format;
    while (format = time_formats[i++])
        if (seconds < format[0]) {
            if (typeof format[2] == 'string')
                return format[list_choice];
            else
                return Math.floor(seconds / format[2]) + ' ' + format[1] + ' ' + token;
        }
    return time;
}