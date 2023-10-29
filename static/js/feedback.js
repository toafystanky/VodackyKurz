 $(document).ready(function () {
            // Při načtení dokumentu provede následující kód
            $("#review-form").submit(function (event) {
                event.preventDefault(); // Zamezí výchozímu odeslání formuláře

                var nickname = $("#nickname").val();
                var review = $("#review").val();

                // Odešleme data recenze na server pomocí AJAX
                $.ajax({
                    type: "POST",
                    url: "/recenze",
                    data: {
                        nickname: nickname,
                        review: review
                    },
                    success: function (response) {
                        // Zobrazíme zprávu o úspěšném odeslání
                        alert("Recenze byla úspěšně odeslána!");
                        location.reload();
                    },
                    error: function (xhr, status, error) {
                        // Zobrazíme chybovou zprávu v alertu
                        alert(xhr.responseText);
                    }
                });
            });

            // Počet znaků
            $("#review").on("input", function () {
                var maxChars = 400; // Maximální povolený počet znaků
                var currentChars = $(this).val().length;
                var remainingChars = maxChars - currentChars;
                $("#char-count").text("Zbývá znaků: " + remainingChars);

                if (remainingChars < 0) {
                    $("#char-count").addClass("text-danger");
                } else {
                    $("#char-count").removeClass("text-danger");
                }
            });
        });