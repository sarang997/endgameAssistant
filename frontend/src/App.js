
import React, { useState, useEffect } from 'react';
import Chessboard from 'chessboardjsx';

function App() {
    const [fenData, setFenData] = useState([]);  // This will now store both FEN and score
    const [currentIndex, setCurrentIndex] = useState(0);  // To keep track of the current board

    useEffect(() => {
        // Assuming fen.txt is in the public directory of your React app
        fetch('/fen.txt')
            .then(response => response.text())
            .then(data => {
                const lines = data.split('\n');
                const fensAndScores = lines.map(line => {
                    try {
                        return JSON.parse(line);
                    } catch (e) {
                        return null;
                    }
                }).filter(item => item);
                setFenData(fensAndScores);
            });
    }, []);

    const nextBoard = () => {
        setCurrentIndex(prevIndex => (prevIndex + 1) % fenData.length);  // Loop back to the start after the last board
    }

    const previousBoard = () => {
        setCurrentIndex(prevIndex => (prevIndex - 1 + fenData.length) % fenData.length);  // Loop to the end if at the start
    }

    const currentFen = fenData[currentIndex]?.FEN || '';
    const activeColor = currentFen.split(' ')[1];
    const orientation = activeColor === 'w' ? 'white' : 'black';
    const engineEval = fenData[currentIndex]?.score || '';

    return (
        <div className="App" style={{ background: '#f0e4d7', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ marginBottom: '10px' }}>
                <span style={{ fontSize: '18px', fontWeight: 'bold' }}>FEN {currentIndex + 1}</span>
                <span style={{ marginLeft: '20px', fontSize: '16px', color: '#607d8b' }}>Engine Eval: {engineEval}</span>
            </div>
            <div style={{ width: '480px', background: '#fff', boxShadow: '0px 0px 15px rgba(0, 0, 0, 0.2)', padding: '20px', borderRadius: '10px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Chessboard position={currentFen} width={450} orientation={orientation} />
                <div style={{ display: 'flex', marginTop: '20px' }}>
                    <button onClick={previousBoard} style={{ padding: '10px 20px', fontSize: '24px', borderRadius: '5px', background: 'rgba(96, 125, 139, 0.8)', color: '#fff', border: 'none', cursor: 'pointer', marginRight: '10px' }}>←</button>
                    <button onClick={nextBoard} style={{ padding: '10px 20px', fontSize: '24px', borderRadius: '5px', background: 'rgba(96, 125, 139, 0.8)', color: '#fff', border: 'none', cursor: 'pointer' }}>→</button>
                </div>
            </div>
        </div>
    );
}

export default App;
