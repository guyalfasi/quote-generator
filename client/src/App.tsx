import { useEffect, useState } from 'react';
import axios from 'axios';

import './App.scss';



function App() {
	const [characters, setCharacters] = useState<string[]>([]);
	const [image, setImage] = useState<string | null>(null);
	const [character, setCharacter] = useState<string>('');
	const [loading, setLoading] = useState<boolean>(false);
	const [error, setError] = useState<string | null>(null);

	const generateImage = async () => {
		setLoading(true);
		setError(null);
		try {
			const response = await axios.post('http://localhost:5000/generate', { character, quote: 'Hello World' }, { responseType: 'blob' });
			const url = URL.createObjectURL(response.data);
			setImage(url);
		} catch (err) {
			console.error('Error generating image:', err);
			setError('Failed to generate the image. Please try again.');
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		axios.get('http://localhost:5000/characters')
			.then((response) => setCharacters(response.data))
			.catch((err) => {
				console.error('Error fetching characters:', err);
				setError('Failed to fetch characters. Please try again later.');
			});
	}, []);

	return (
		<div className="app">
			<h1>Quote Generator</h1>

			{error && <p className="error">{error}</p>}

			<div>
				{loading ? (<p>Loading...</p>) : (<img id="quote-image" src={image || './quote.png'} alt="quote" />)}
			</div>

			<div>
				<label htmlFor="character-select">Select Character:</label>
				<select
					id="character-select"
					value={character}
					onChange={(e) => setCharacter(e.target.value)}
				>
					<option value="">--Choose a character--</option>
					{characters?.map((char) => (
						<option key={char.name} value={char.name}>
							{char.name}
						</option>
					))}
				</select>
			</div>

			<button onClick={generateImage} disabled={loading || !character}>
				{loading ? 'Generating...' : 'Generate'}
			</button>
		</div>
	);
}

export default App;
