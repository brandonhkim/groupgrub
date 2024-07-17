import styles from './CategoryCard.module.css';

function CategoryCard({ categoryName, categoryIsMine, index, deleteSocketCategory}) {
    const removeBtnOnClick = () => deleteSocketCategory(index, categoryName)
    return (
        <div className={styles.cardContainer}>
            { categoryIsMine && <button className={styles.removeBtn} onClick={removeBtnOnClick}> X </button> }

            <h2>{categoryName}</h2>
        </div>
    )
}

export default CategoryCard