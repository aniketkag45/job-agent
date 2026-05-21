import Sidebar from "./Sidebar"

import DashboardHeader from "./DashboardHeader"


function DashboardLayout({ children }) {

  return (

    <div className="flex min-h-screen bg-[#030712]">


      {/* Sidebar */}

      <Sidebar />


      {/* Main Area */}

      <div className="flex-1 flex flex-col">


        {/* Header */}

        <DashboardHeader />


        {/* Page Content */}

        <main className="flex-1 p-8 overflow-y-auto">

          {children}

        </main>

      </div>

    </div>
  )
}

export default DashboardLayout