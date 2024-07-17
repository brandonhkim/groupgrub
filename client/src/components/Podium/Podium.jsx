import styles from './Podium.module.css';


function Podium({ topBusinesses }) {
    topBusinesses = topBusinesses.slice(0, 3);
    const goldBusiness = topBusinesses[0][0];
    const silverBusiness = topBusinesses[1][0];
    const bronzeBusiness = topBusinesses[2][0];

    const goldVotes = topBusinesses[0][1];
    const silverVotes = topBusinesses[1][1];
    const bronzeVotes = topBusinesses[2][1];

    return (
        <div className={styles.container}>
            <div className={styles.silverPodium} >
                <div className={styles.businessInfo}>
                    <img src={silverBusiness["image_url"]} alt='2nd business'/>
                    <p>{silverBusiness["name"]}</p>
                    <p>{silverBusiness["address"]}</p>
                </div>
                <p className={styles.popularityCnt}>
                    {silverVotes} votes
                </p>
            </div>
            <div className={styles.goldPodium} >
                <div className={styles.businessInfo}>
                    <img src={goldBusiness["image_url"]} alt='1st business'/>
                    <p>{goldBusiness["name"]}</p>
                    <p>{goldBusiness["address"]}</p>
                </div>
                <p className={styles.popularityCnt}>
                    {goldVotes} votes
                </p>
            </div>
            <div className={styles.bronzePodium} >
                <div className={styles.businessInfo}>
                    <img src={bronzeBusiness["image_url"]} alt='3rd business'/>
                    <p>{bronzeBusiness["name"]}</p>
                    <p>{bronzeBusiness["address"]}</p>
                </div>
                <p className={styles.popularityCnt}>
                    {bronzeVotes} votes
                </p>
            </div>
        </div>
    );
}

export default Podium;