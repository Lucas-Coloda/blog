$(document).ready(function(){
	$(".content-markdown").each(function(){
	    var content = $(this).text()
		var markedContent = marked(content)
		$(this).html(markedContent)
	})
	$(".content-markdown img").each(function(){
		$(this).addClass("img-responsive")
	})
})
