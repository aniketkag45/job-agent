import {

  useState,useEffect

} from "react"
import { SavedJobsContext } from "./savedjobscontext"



function SavedJobsProvider({

  children
}) {

  const [savedJobs, setSavedJobs] =
useState(() => {

  const storedJobs =
  localStorage.getItem("savedJobs")

  return storedJobs
    ? JSON.parse(storedJobs)
    : []
})

useEffect(() => {

  localStorage.setItem(

    "savedJobs",

    JSON.stringify(savedJobs)
  )

}, [savedJobs])


  const toggleSaveJob = (job) => {

    const alreadySaved =
    savedJobs.some(

      (savedJob) =>

        savedJob.role === job.role &&

        savedJob.company === job.company
    )


    if (alreadySaved) {

      setSavedJobs(

        savedJobs.filter(

          (savedJob) =>

            !(
              savedJob.role === job.role &&
              savedJob.company === job.company
            )
        )
      )

    } else {

      setSavedJobs([
        ...savedJobs,
        job
      ])
    }
  }


  return (

    <SavedJobsContext.Provider
      value={{
        savedJobs,
        toggleSaveJob
      }}
    >

      {children}

    </SavedJobsContext.Provider>
  )
}

export default SavedJobsProvider