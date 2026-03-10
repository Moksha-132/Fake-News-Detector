$(document).ready(function () {

    // File upload visual feedback
    $('#image-input').on('change', function (e) {
        let fileName = e.target.files[0]?.name;
        if (fileName) {
            $('#image-label').text(fileName).addClass('text-purple-300');
            $('#image-dropzone i').removeClass('fa-image').addClass('fa-file-image text-purple-400');
            $('#image-dropzone').addClass('bg-purple-500/10 border-purple-500/50');
        }
    });

    $('#video-input').on('change', function (e) {
        let fileName = e.target.files[0]?.name;
        if (fileName) {
            $('#video-label').text(fileName).addClass('text-pink-300');
            $('#video-dropzone i').removeClass('fa-video').addClass('fa-file-video text-pink-400');
            $('#video-dropzone').addClass('bg-pink-500/10 border-pink-500/50');
        }
    });

    // Form Submission
    $('#analysis-form').on('submit', function (e) {
        e.preventDefault();

        let hasText = $('#news_text').val().trim().length > 0;
        let hasImage = $('#image-input')[0].files.length > 0;
        let hasVideo = $('#video-input')[0].files.length > 0;

        if (!hasText && !hasImage && !hasVideo) {
            $('#error-box').text('Please provide at least some text, image, or video evidence to analyze.').removeClass('hidden');
            return;
        }

        $('#error-box').addClass('hidden');

        // Show loading screen
        $('#loading-overlay').removeClass('hidden');

        // Setup sequential status updates
        let timeouts = [];
        $('.status-item').each(function () {
            let item = $(this);
            let delay = parseInt(item.data('delay'));

            if (delay > 0) {
                timeouts.push(setTimeout(() => {
                    item.removeClass('opacity-50');
                    item.find('.pending-icon').addClass('hidden');
                    item.find('.active-icon').removeClass('hidden');

                    // Update previous item to done
                    let prev = item.prev();
                    if (prev.length) {
                        prev.find('.active-icon').addClass('hidden');
                        prev.find('.pending-icon').removeClass('hidden outline-none cursor-default').addClass('text-blue-500 fa-check-circle').removeClass('fa-circle text-gray-600');
                    }
                }, delay));
            } else {
                item.removeClass('opacity-50');
                item.find('.pending-icon').addClass('hidden');
                item.find('.active-icon').removeClass('hidden');
            }
        });

        // Prepare data
        var formData = new FormData(this);

        // Submit to API
        $.ajax({
            url: '/predict',
            type: 'POST',
            data: formData,
            success: function (response) {
                // Save to local storage for result page
                localStorage.setItem('analysisResult', JSON.stringify(response));

                // Allow final animation to play 
                setTimeout(() => {
                    window.location.href = '/result';
                }, 1000);
            },
            error: function (xhr) {
                // Hide loader
                $('#loading-overlay').addClass('hidden');

                // Clear timeouts
                timeouts.forEach(clearTimeout);

                let errorMsg = "An error occurred during analysis.";
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                $('#error-box').text(errorMsg).removeClass('hidden');
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});
