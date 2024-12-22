// image loader
// NOTE: var anime_list must be a json object defined in the html file in script tag

const build_graphql_query = (anime_list) => {
    let query = "";

    anime_list.forEach((anime) => {
        let anime_name = anime.title;

        if (anime_name.includes("(")) {
            anime_name = anime_name.split("(")[0];
        }

        if (anime_name.includes(":")) {
            anime_name = anime_name.split(":")[0];
        }

        query += `
        id_${anime.id}: Media(search: "${anime_name}", type: ANIME) {
            coverImage{
                large
            }
        }
        `;
    });

    query = `
    query Media{
        ${query}
    }
    `;

    return query;
};

const fetch_graphql_query = async (query) => {
    const url = "https://graphql.anilist.co";
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        body: JSON.stringify({
            query: query,
        }),
    };

    const response = await fetch(url, options);
    const data = await response.json();
    return data;
};

const parse_graphql_data = (data) => {
    const parsed_data = [];

    for (const key in data.data) {
        if (data.data[key]?.coverImage?.large) {
            parsed_data.push({
                id: key.split("_")[1],
                src: data.data[key].coverImage.large,
            });
        }
    }

    return parsed_data;
};

const set_image_src = (anime_id, src) => {
    try {
        const anime_card = document.getElementById(`anime-card-${anime_id}`);
        anime_card.querySelector(".anime-card-image").src = src;
    } catch (error) {
        // console.error(error);
    }
};

const main = async () => {
    const query = build_graphql_query(anime_list);
    const data = await fetch_graphql_query(query);
    const parsed_data = parse_graphql_data(data);

    for (const anime of parsed_data) {
        set_image_src(anime.id, anime.src);
    }
};

if (anime_list?.length > 0) {
    main();
}
