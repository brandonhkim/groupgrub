function range(minVal, maxVal, inc, priceFlag) {
    let values = []
    while(minVal <= maxVal) {
        if(priceFlag) { values.push("$".repeat(minVal)) }
        else { values.push(minVal); }
        minVal += inc;
    }
    return values
}

function LobbyDropdown({ option, setOption, heading, prefix, minVal, maxVal, increment, modifiable=true}) {
    return (
        <div>
            <h3>{heading}</h3>
            {
                <select value={option} disabled={ !modifiable } onChange={(event) => {
                    if (option !== event.target.value ) {
                        setOption(event.target.value)
                    }
                } }> {
                    range(minVal, maxVal, increment, prefix === "price" ? true : false).map( (val, ind) => 
                        <option key={ prefix + ind } value={ val }> { val } </option> )}
                </select>
            }
        </div>
    )
}

export default LobbyDropdown