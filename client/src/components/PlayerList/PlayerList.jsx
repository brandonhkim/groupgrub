import styles from './PlayerList.module.css'

function PlayerList({players}) {
    console.log("players", players)
    return (
        <div className={styles.container}>
            <ul className={styles.column}>
            {
                players.length > 0
                ? players.map((player) => {
                    return (
                        <li className={styles.nickname} key={`${player}Player`}>
                            { player }
                        </li>
                    );
                })
                : null
            }
            </ul>
        </div>
    )
}

export default PlayerList;