import styles from './LobbyDropdown.module.css'

/* ~ Builds dropdown options ~ */
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
    const handleDropdownChange = (e) => {
        if (option !== e.target.value ) {
            setOption(e.target.value)
        }}

    return (
        <div className={styles.lobbyDropdown}>
            <h3 className={styles.heading}>{heading}</h3>
            {
                <select value={option} disabled={ !modifiable } onChange={ handleDropdownChange }> 
                {
                    range(minVal, maxVal, increment, prefix === "price" ? true : false).map( (val, ind) => 
                        <option key={ prefix + ind } value={ val }> { val } </option> )
                }
                </select>
            }
        </div>
    )
}

export default LobbyDropdown