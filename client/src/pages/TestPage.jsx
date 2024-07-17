import Podium from "../components/Podium/Podium"

function TestPage() {
    const mewo = {
        name: "mewo",
        image_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo1lakk8v57vUdqcF9fDAOwJuLHmv5ka8MRg&s",
        price: "$$$$", 
        phone: "(666)123-45678",
        address: "123 Kitty St.\n White Space, Mind Space 666"
    }
    const daijin = {
        name: "daijin",
        image_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJQbvingkXyK2nDMVLROzJ12Z6E4EcFKVSmQ&s",
        price: "$$$$", 
        phone: "(123)456-7890",
        address: "123 Kitty St.\n Suzume, Japan 777"
    }

    const businesses = [
        [mewo, 10],
        [daijin, 7],
        [daijin, 5]
    ]
    return (
        <div>
            <h1> My test bench</h1>
            <Podium topBusinesses={businesses} />
            <ol>
                {
                    businesses.map(element => 
                        <li>{element[0].name}</li>
                    )
                }
            </ol>
        </div>
    )
}

export default TestPage