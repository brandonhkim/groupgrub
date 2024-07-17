import styles from './BusinessCard.module.css'

function BusinessCard({name, image_url, price, phone}) {
    return (
        <div className={styles.container}>
            <img src={image_url} alt='business'/>
            <p>{name}, {price}</p>
            <p>{phone}</p>
        </div>
    )
}
export default BusinessCard;