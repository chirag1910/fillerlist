// image loader
anime_list = document.querySelectorAll(".anime-card");
for (let i = 0; i < anime_list.length; i++) {
    let anime_name = anime_list[i].querySelector(
        ".anime-card-info .anime-card-info-name"
    ).innerText;
    let anime_image = anime_list[i].querySelector(".anime-card-image");
    get_image_src(anime_name, anime_image);
}

function get_image_src(anime_name, anime_image) {
    if (anime_name.includes("(")) {
        anime_name = anime_name.split("(")[0];
    }

    var query = `
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                coverImage{
                    large
                }
            }
        }
    `;

    var variables = {
        search: anime_name,
    };

    var url = "https://graphql.anilist.co",
        options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
            body: JSON.stringify({
                query: query,
                variables: variables,
            }),
        };

    fetch(url, options)
        .then(handleResponse)
        .then(handleData)
        .catch(handleError);

    function handleResponse(response) {
        return response.json().then(function (json) {
            return response.ok ? json : Promise.reject(json);
        });
    }

    function handleData(data) {
        anime_image.src = data["data"]["Media"]["coverImage"]["large"];
    }

    function handleError(error) {
        anime_image.src =
            "https://s4.anilist.co/file/anilistcdn/character/large/default.jpg";
    }
}
