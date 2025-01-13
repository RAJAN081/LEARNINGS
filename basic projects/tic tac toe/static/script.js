document.addEventListener("DOMContentLoaded", () => {
    const board = document.getElementById("board");
    const status = document.getElementById("status");
    const playerInput = document.getElementById("player-input");
    const startBtn = document.getElementById("start-btn");
    const startModal = document.getElementById("start-modal");
    const playerScore = document.getElementById("player-score");
    const aiScore = document.getElementById("ai-score");

    let playerName = "Player";
    let gameActive = false;

    // Initialize the game
    function initializeBoard() {
        board.innerHTML = ""; // Clear the board
        for (let i = 0; i < 9; i++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.dataset.index = i;
            board.appendChild(cell);
        }
    }

    // Fetch data from the server
    async function fetchData(url, data) {
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return await response.json();
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    // Handle cell clicks
    board.addEventListener("click", async (event) => {
        if (!gameActive) return;

        const target = event.target;
        if (!target.classList.contains("cell")) return;

        const index = parseInt(target.dataset.index, 10);
        const result = await fetchData("/play", { move: index });

        if (result) {
            updateBoard(result.board);
            if (result.winner) {
                updateGameStatus(result.winner);
                updateScores(result.scores);
            } else {
                updateGameStatus(null);
            }
        }
    });

    // Update the board visually
    function updateBoard(boardState) {
        const cells = document.querySelectorAll(".cell");
        cells.forEach((cell, index) => {
            cell.textContent = boardState[index];
        });
    }

    // Update the scores
    function updateScores(scores) {
        document.getElementById("player-score").textContent = scores.Player;
        document.getElementById("ai-score").textContent = scores.AI;
    }

    // Update the game status
    function updateGameStatus(winner) {
        if (winner) {
            status.textContent = `${winner} wins!`;
            gameActive = false;
        } else {
            status.textContent = "Your turn!";
        }
    }

    // Start a new game
    startBtn.addEventListener("click", async () => {
        playerName = playerInput.value || "Player";
        startModal.style.display = "none";
        const result = await fetchData("/start", { player_name: playerName });
        if (result) {
            updateScores(result.scores);
            initializeBoard();
            gameActive = true;
            status.textContent = "Your turn!";
        }
    });

    // Initialize the modal and game
    startModal.style.display = "block";
});
