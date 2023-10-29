    // Funkce pro návrat zpět v historii prohlížeče
        function goBack() {
            window.history.back();
        }

        // Funkce pro kontrolu dostupnosti přezdívky
        $(document).ready(function () {
            $("#nick").on("input", function () {
                var nickname = $(this).val();
                if (nickname.length > 0) {
                    // Odešleme AJAX požadavek pro kontrolu dostupnosti přezdívky
                    $.ajax({
                        type: "POST",
                        url: "/check_nickname",
                        data: { nickname: nickname },
                        success: function (response) {
                            if (response === "taken") {
                                $("#nickname-warning").text("Přezdívka je již zaregistrována.");
                            } else if (response === "invalid") {
                                $("#nickname-warning").text("Přezdívka obsahuje nepovolené znaky.");
                            } else if (response === "short") {
                                $("#nickname-warning").text("Přezdívka je moc krátká.");
                            } else if (response === "long") {
                                $("#nickname-warning").text("Přezdívka je moc dlouhá.");
                            } else {
                                $("#nickname-warning").text("");
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log(xhr.responseText);
                        }
                    });
                } else {
                    // Smaže varovnou zprávu, pokud je přezdívka příliš krátká
                    $("#nickname-warning").text("");
                }
            });

            // Funkce pro kontrolu jména
            $("#name").on("input", function () {
                var name = $(this).val();
                if (name.length > 0) {
                    // Odešleme AJAX požadavek pro kontrolu jména
                    $.ajax({
                        type: "POST",
                        url: "/check_name",
                        data: { name: name },
                        success: function (response) {
                            if (response === "invalid") {
                                $("#name-warning").text("Jméno obsahuje nepovolené znaky.");
                            } else if (response === "long") {
                                $("#name-warning").text("Jméno je moc dlouhé.");
                            } else if (response === "short") {
                                $("#name-warning").text("Jméno je moc krátké.");
                            } else {
                                $("#name-warning").text("");
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log(xhr.responseText);
                        }
                    });
                } else {
                    // Smaže varovnou zprávu, pokud je jméno příliš krátké
                    $("#name-warning").text("");
                }
            });

            // Funkce pro kontrolu příjmení
            $("#last_name").on("input", function () {
                var last_name = $(this).val();
                if (last_name.length > 0) {
                    $.ajax({
                        type: "POST",
                        url: "/check_last_name",
                        data: { last_name: last_name },
                        success: function (response) {
                            if (response === "invalid") {
                                $("#last-name-warning").text("Příjmení obsahuje nepovolené znaky.");
                            } else if (response === "long") {
                                $("#last-name-warning").text("Příjmení je moc dlouhé.");
                            } else if (response === "short") {
                                $("#last-name-warning").text("Příjmení je moc krátké.");
                            }  else {
                                $("#last-name-warning").text("");
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log(xhr.responseText);
                        }
                    });
                } else {
                    $("#last-name-warning").text("");
                }
            });

            // Funkce pro kontrolu e-mailu
            $("#email").on("input", function () {
                var email = $(this).val();
                if (email.length >= 2) {
                    // Odešleme AJAX požadavek pro kontrolu e-mailu
                    $.ajax({
                        type: "POST",
                        url: "/check_email",
                        data: {email: email},
                        success: function (response) {
                            if (response === "taken") {
                                $("#email-warning").text("Email je již zaregistrován.");
                            } else if (response === 'invalid') {
                                $("#email-warning").text("Email je v neplatném formátu.")
                            } else {
                                $("#email-warning").text("");
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log(xhr.responseText);
                        }
                    });
                } else {
                    // Smaže varovnou zprávu, pokud je e-mail příliš krátký
                    $("#email-warning").text("");
                }
            });

            // Funkce pro kontrolu společníka na kanoe
            $("#kanoe_kamarad").on("input", function () {
                var kanoe_kamarad = $(this).val();
                if (kanoe_kamarad.length >= 1) {
                    $.ajax({
                        type: "POST",
                        url: "/check_companion",
                        data: {kanoe_kamarad: kanoe_kamarad},
                        success: function (response) {
                            if (response === "True") {
                                $("#kanoe-warning").text("Společník byl již vybrán jiným účastníkem.");
                            } else if (response === "False") {
                                $("#kanoe-warning").text("Společník na lodi není registrován.");
                            } else if (response === "Invalid") {
                                $("#kanoe-warning").text("Společník na lodi již má svého účastníka.");
                            } else {
                                $("#kanoe-warning").text("");
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log(xhr.responseText);
                        }
                    });
                } else {
                    // Smaže varovnou zprávu, pokud je vstup příliš krátký
                    $("#kanoe-warning").text("");
                }
            });

            // Funkce pro změnu hodnoty v dropdownu
            $("#je_plavec").change(function () {
                console.log("Dropdown změněn"); // Přidáno pro ladění
                var je_plavec = parseInt($(this).val()); // Převede na celé číslo
                console.log("Hodnota je_plavec: " + je_plavec); // Přidáno pro ladění
                if (je_plavec === 0) {
                    console.log("Odesílání AJAX požadavku"); // Přidáno pro ladění
                    // Odešleme AJAX požadavek pro kontrolu, zda je osoba plavcem
                    $.ajax({
                        type: "POST",
                        url: "/check_swimmer",
                        data: {je_plavec: je_plavec},
                        success: function (response) {
                            console.log("Odpověď: " + response); // Přidáno pro ladění
                            if (response === "invalid") {
                                $("#swimmer-warning").text("Musíte umět plavat.");
                            } else {
                                $("#swimmer-warning").text("");
                            }
                        },
                        error: function (xhr, status, error) {
                            console.log(xhr.responseText);
                        }
                    });
                } else {
                    $("#swimmer-warning").text("");
                }
            });

            // Funkce pro odeslání formuláře
            $("#registration-form").submit(function (event) {
                event.preventDefault(); // Zamezí výchozímu odeslání formuláře

                var nickname = $("#nick").val();
                var isSwimmer = $("#je_plavec").val();
                var canoeCompanion = $("#kanoe_kamarad").val();
                var class_name = $("#class").val();
                var name = $("#name").val();
                var last_name = $("#last_name").val();
                var email = $("#email").val();

                if (isSwimmer === "0" || nickname.length < 2) {
                    alert("Chyba: Neplatné údaje!");
                    return;
                }

                // Validace e-mailu pomocí regulárního výrazu
                var emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0.9.-]+\.[A-Za-z]{2,}$/;
                if (!email.match(emailPattern)) {
                    alert("Chyba: Neplatná e-mailová adresa!");
                    return;
                }

                // Pokračujeme s odesláním formuláře, pokud všechny kontroly projdou
                // Odešleme data registrace na server pomocí AJAX
                $.ajax({
                    type: "POST",
                    url: "/registrace",
                    data: {
                        name: name,
                        last_name: last_name,
                        nick: nickname,
                        je_plavec: isSwimmer,
                        kanoe_kamarad: canoeCompanion,
                        email: email,
                        class: class_name
                    },
                    success: function (response) {
                        alert("Registrace úspěšná!");
                        goBack();
                    },
                    error: function (xhr, status, error) {
                        alert(xhr.responseText);
                    }
                });
            });
        });