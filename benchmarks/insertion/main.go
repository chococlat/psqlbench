package main

import (
	"database/sql"
	"fmt"
	"log"
	"sync"
	"time"
    "math/rand/v2"
	_ "github.com/lib/pq"
)

var counter = 0

const (
    connStr       = "host=localhost port=5432 user=postgres password=password dbname=postgres sslmode=disable"
    numWorkers    = 80       // Number of concurrent workers
    totalInserts  = 10000000  // Total number of inserts
    printInterval = 10000    // Print count every 10,000 inserts
)

func setupDB() (*sql.DB, error) {
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        return nil, err
    }

    // Set connection pool limits
    db.SetMaxOpenConns(180) // Limit to 100 concurrent open connections
    db.SetMaxIdleConns(60)  // Limit to 50 idle connections

    return db, nil
}

func main() {
    db, err := setupDB()
    if err != nil {
        log.Fatalf("failed to connect to db: %v", err)
    }
    defer db.Close()

    var wg sync.WaitGroup
    wg.Add(numWorkers)

    var totalInserted int64
    var mu sync.Mutex

    startTime := time.Now()

    for i := 0; i < numWorkers; i++ {
        go func(workerID int) {
            defer wg.Done()

            localInserted := 0
            for j := 0; j < totalInserts/numWorkers; j++ {

                _, err = db.Exec(fmt.Sprintf(`
                UPDATE relational.tokens
                SET token = 'changed'
                WHERE id = %v;
                `,rand.IntN(2000000)))
                if err != nil {
                    log.Printf("worker %d: failed to insert: %v", workerID, err)
                }
				counter++
				if (counter%10000 == 0){

					fmt.Println(counter)
				}


                localInserted++

                
            }

            mu.Lock()
            totalInserted += int64(localInserted)
            mu.Unlock()
        }(i)
    }

    wg.Wait()

    elapsed := time.Since(startTime).Seconds() 
    log.Printf("Total inserts completed: %d", totalInserted)
    log.Printf("Time taken: %v", elapsed)
	log.Printf("per second: %v", float64(totalInserted) / elapsed)
}
