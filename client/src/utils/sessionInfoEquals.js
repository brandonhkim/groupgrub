export default (one, two) => {
    return one["nickname"] === two["nickname"] && one["session_ID"] === two["session_ID"];
}