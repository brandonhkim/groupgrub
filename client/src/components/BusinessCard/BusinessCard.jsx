import styles from './BusinessCard.module.css'

function BusinessCard({name, image_url, price, phone}) {
    return (
        <div className={styles.container}>
            <img src={image_url} alt='business'/>
            <p className={styles.preventSelect}>{name}, {price}</p>
            <p className={styles.preventSelect}>{phone}</p>
        </div>
    )
}
export default BusinessCard;