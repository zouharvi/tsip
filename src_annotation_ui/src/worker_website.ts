let title_area_table = $("#title_area_table_body")

function load_headers() {
    $("#progress").html(`
        <strong>Progress:</strong> ${globalThis.data_i + 1}/${globalThis.data.length},
        <strong>UID:</strong> ${globalThis.uid},
        <strong>mode:</strong> ${globalThis.data_now["mode"]}
    `)
    $("#abstract").text(globalThis.data_now["abstract"])
}

function load_cur_abstract() {
    load_headers()

    switch (globalThis.data_now["mode"]) {
        case "all_direct_noref": load_cur_abstract_all_direct(); break;
        case "all_direct_ref": load_cur_abstract_all_direct_ref(); break;
        case "pair_direct_noref": load_cur_abstract_all_direct(); break;
        case "pair_direct_ref": load_cur_abstract_all_direct_ref(); break;
        case "pair_rank_noref": load_cur_abstract_rank_pair(); break;
        case "all_rank_noref": load_cur_abstract_all_rank(); break;
        case "all_rank_ref": load_cur_abstract_all_rank_ref(); break;
    }
}

function load_cur_abstract_all_direct() {
    title_area_table.html("")
    title_area_table.append($("<tr><td>Title</td><td>Score</td></tr>"));

    globalThis.data_now["titles_order"].forEach((title_order: number, title_i: number) => {
        let new_an = $(`
            <tr>
                <td>• ${globalThis.data_now["titles"][title_order]}</td>
                <td><span id="q_${title_i}_val">x</span><input id="q_${title_i}" type="range" min="0" max="4" step="1"></td>
            </tr>
        `)
        title_area_table.append(new_an);
        bind_labels_direct(title_i);
    })


    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });

        // space for comments
        globalThis.data_now["response"].push("")
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}


function load_cur_abstract_all_direct_ref() {
    title_area_table.html("")
    title_area_table.append($("<tr><td>Title</td><td>Score</td></tr>"));

    if (globalThis.data_now["titles_order"][0] != 0) {
        console.error(`The first in title in order is not 0 but ${globalThis.data_now["titles_order"][0]} and you requested reference comparison.`)
    }

    globalThis.data_now["titles_order"].forEach((title_order: number, title_i: number) => {
        let new_an;
        if (title_i == 0) {
            new_an = $(`
            <tr>
                <td>• <b>Reference:</b> ${globalThis.data_now["titles"][title_order]}</td><td>-</td>
            </tr>
        `)
        } else {
            new_an = $(`
                <tr>
                    <td>• ${globalThis.data_now["titles"][title_order]}</td>
                    <td><span id="q_${title_i}_val">x</span><input id="q_${title_i}" type="range" min="0" max="4" step="1"></td>
                </tr>
            `)
        }
        title_area_table.append(new_an);
        bind_labels_direct(title_i);
    })


    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });

        // space for comments
        globalThis.data_now["response"].push("")
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}


function load_cur_abstract_rank_pair() {
    title_area_table.html("")
    if (globalThis.data_now["titles_order"].length != 2) {
        console.error(`Titles count is not 2 but ${globalThis.data_now["titles_order"].length}`)
    }
    title_area_table.append($("<tr><td>Title</td><td>Preference</td></tr>"));

    globalThis.data_now["titles"].forEach((title: string, title_i: number) => {
        let new_an = $(`
            <tr>
                <td>• ${title}</td>
                <td><input id="q_${title_i}" name="titles_rank" type="radio"></td>
            </tr>
        `)
        title_area_table.append(new_an);
        bind_labels_rank_pair(title_i);
    })

    // todo this won't load correctly
    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}


function load_cur_abstract_all_rank() {
    title_area_table.html("")
    let radio_names = globalThis.data_now["titles_order"].map((_title_order: string, rank: number) => {
        return `${rank + 1}`;
    }).join("&nbsp;&nbsp;&nbsp;");
    title_area_table.append($(`<tr><td>Title</td><td>Rank:<br>${radio_names}</td></tr>`));

    globalThis.data_now["titles_order"].forEach((title_order: string, title_i: number) => {
        let radios = globalThis.data_now["titles_order"].map((_title_order: string, rank: number) => {
            return `<input id="q_${title_i}_${rank}" name="titles_rank_${title_i}" title_rank="${rank}" type="radio" style="">`;
        }).join("");
        let new_an = $(`
            <tr>
                <td>• ${globalThis.data_now["titles"][title_order]}</td>
                <td>${radios}</td>
            </tr>
        `)
        title_area_table.append(new_an);
        bind_labels_rank(title_i, globalThis.data_now["titles_order"].length);
    })

    // todo this won't load correctly
    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}


function load_cur_abstract_all_rank_ref() {
    title_area_table.html("")
    let radio_names = globalThis.data_now["titles_order"].filter((rank: number) => rank != 0).map((_title_order: string, rank: number) => {
        return `${rank+1}`;
    }).join("&nbsp;&nbsp;&nbsp;");
    title_area_table.append($(`<tr><td>Title</td><td>Rank:<br>${radio_names}</td></tr>`));

    if (globalThis.data_now["titles_order"][0] != 0) {
        console.error(`The first in title in order is not 0 but ${globalThis.data_now["titles_order"][0]} and you requested reference comparison.`)
    }

    globalThis.data_now["titles_order"].forEach((title_order: string, title_i: number) => {
        let new_an;
        if (title_i == 0) {
            new_an = $(`
            <tr>
                <td>• <b>Reference:</b> ${globalThis.data_now["titles"][title_order]}</td><td>-</td>
            </tr>
        `)
        } else {
            let radios = globalThis.data_now["titles_order"].map((_title_order: string, rank: number) => {
                // skip the first one, for reference
                if (rank == 0)
                    return "";
                return `<input id="q_${title_i}_${rank}" name="titles_rank_${title_i}" title_rank="${rank}" type="radio" style="">`;
            }).join("");
            new_an = $(`
                <tr>
                    <td>• ${globalThis.data_now["titles"][title_order]}</td>
                    <td>${radios}</td>
                </tr>
            `)
        }
        title_area_table.append(new_an);
        bind_labels_rank(title_i, globalThis.data_now["titles_order"].length, 1);
    })

    // todo this won't load correctly
    if (!globalThis.data_now.hasOwnProperty("response")) {
        globalThis.data_now["response"] = []
        globalThis.data_now["titles_order"].forEach((title: string) => {
            // set default response
            globalThis.data_now["response"].push(-1);
        });
    }

    // resets values
    globalThis.data_now["titles_order"].forEach((title: string, title_i: number) => {
        $("#q_" + title_i.toString()).val(globalThis.data_now["response"][title_i]);
    })
}

function bind_labels_direct(title_i: number) {
    $("#q_" + title_i.toString()).on('input change', function () {
        let val = parseInt($(this).val() as string);
        globalThis.data_now["response"][title_i] = val;

        let slider_obj_val = $("#q_" + title_i.toString() + "_val");
        slider_obj_val.text(val)
    });

    // special handling of default "empty" value
    $("#q_" + title_i.toString()).on('click', function () {
        if (globalThis.data_now["response"][title_i] == -1) {
            globalThis.data_now["response"][title_i] = 0;

            let val = parseInt($(this).val() as string);
            console.log(val)
            let slider_obj_val = $("#q_" + title_i.toString() + "_val");
            slider_obj_val.text(val)
        }
    });
}

function bind_labels_rank_pair(title_i: number) {
    $("#q_" + title_i.toString()).on('input change', function () {
        let val = $(this).is(":checked") ? 1 : 0;
        if (val != 1) {
            console.error(`The currently checked button (${title_i}) is not 1 but ${val}`)
        }
        globalThis.data_now["response"][title_i] = val;
        // set the other to 0
        globalThis.data_now["response"][(title_i + 1) % 2] = 0;
    });
}

function bind_labels_rank(title_i: number, title_total: number, start_rank: number = 0) {
    for (let rank = start_rank; rank < title_total; rank++) {
        $(`#q_${title_i}_${rank}`).on('input change', function () {
            let val = $(this).is(":checked") ? 1 : 0;
            if (val != 1) {
                console.error(`The currently checked button (${title_i}) is not 1 but ${val}`)
            }

            for (let title_other = 0; title_other < title_total; title_other++) {
                if (title_i == title_other) {
                    continue;
                }
                let other_same = $(`#q_${title_other}_${rank}`)
                if (other_same.is(":checked")) {
                    other_same.prop("checked", false)
                }
            }

            // console.log("My rank is", rank)
            // globalThis.data_now["response"][title_i] = val;
            // // set the other to 0
            // globalThis.data_now["response"][(title_i+1)%2] = 0;
        });
    }
}

function setup() {
    // send current data
    // load next abstract
    $("#but_next").on("click", () => {
        globalThis.data_i += 1;
        if (globalThis.data_i >= globalThis.data.length) {
            alert("You completed the whole queue, thanks! Wait a few seconds to finish synchronization.");
            globalThis.data_i = 0;
        }

        globalThis.data_now = globalThis.data[globalThis.data_i];
        // log_data()
        load_cur_abstract()
    })

    $("#but_prev").on("click", () => {
        globalThis.data_i -= 1;
        // modulo
        if (globalThis.data_i < 0) {
            globalThis.data_i = globalThis.data.length - 1;
        }

        globalThis.data_now = globalThis.data[globalThis.data_i];
        // log_data()
        load_cur_abstract()
    })
}


export { setup, load_cur_abstract }