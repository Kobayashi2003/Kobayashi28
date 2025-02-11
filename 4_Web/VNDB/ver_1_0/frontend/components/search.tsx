"use client"

import * as React from "react"
import { SearchIcon, SlidersHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"

const searchTypes = [
  { value: "vn", label: "Visual Novels" },
  { value: "release", label: "Releases" },
  { value: "character", label: "Characters" },
  { value: "producer", label: "Producers" },
  { value: "staff", label: "Staff" },
]

type BooleanFilter = boolean | null

export function Search() {
  const [searchType, setSearchType] = React.useState("vn")
  const [isSortOpen, setSortOpen] = React.useState(false)
  const [isAdvancedOpen, setAdvancedOpen] = React.useState(false)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Implement search logic
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSearch} className="flex gap-2">
        <Select value={searchType} onValueChange={setSearchType}>
          <SelectTrigger className="w-[180px] bg-[#0F2942]/80 border-white/10 text-white">
            <SelectValue placeholder="Select type" />
          </SelectTrigger>
          <SelectContent>
            {searchTypes.map((type) => (
              <SelectItem key={type.value} value={type.value}>
                {type.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <div className="flex-1 flex gap-2">
          <div className="relative flex-1">
            <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-white/60" />
            <Input
              placeholder="Search..."
              className="pl-9 bg-[#0F2942]/80 border-white/10 text-white placeholder:text-white/60"
            />
          </div>
        </div>

        <Button
          variant="outline"
          size="icon"
          className="bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
          onClick={() => setSortOpen(true)}
        >
          <SlidersHorizontal className="h-4 w-4 text-white" />
        </Button>

        <Button
          variant="outline"
          className="bg-[#0F2942]/80 border-white/10 hover:bg-[#0F2942] hover:border-white/20"
          onClick={() => setAdvancedOpen(true)}
        >
          Advanced
        </Button>
      </form>

      {/* Sort Options Dialog */}
      <Dialog open={isSortOpen} onOpenChange={setSortOpen}>
        <DialogContent className="bg-[#0F2942] text-white border-white/10">
          <DialogHeader>
            <DialogTitle>Sort Options</DialogTitle>
          </DialogHeader>

          <div className="space-y-6 pt-4">
            <div className="space-y-4">
              <Label>Sort By</Label>
              <RadioGroup defaultValue="title">
                {searchType === "vn" && (
                  <>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="title" id="title" />
                      <Label htmlFor="title">Title</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="released" id="released" />
                      <Label htmlFor="released">Release Date</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="rating" id="rating" />
                      <Label htmlFor="rating">Rating</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="votecount" id="votecount" />
                      <Label htmlFor="votecount">Popularity</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="length" id="length" />
                      <Label htmlFor="length">Length</Label>
                    </div>
                  </>
                )}
                {/* Keep other searchType options */}
              </RadioGroup>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Advanced Search Dialog */}
      <Dialog open={isAdvancedOpen} onOpenChange={setAdvancedOpen}>
        <DialogContent className="bg-[#0A1929] text-white border-white/10 max-w-2xl max-h-[80vh]">
          <DialogHeader>
            <DialogTitle className="text-xl">Advanced Search</DialogTitle>
          </DialogHeader>

          <Tabs defaultValue="filters" className="w-full">
            <TabsList className="w-full grid grid-cols-2 bg-[#0F2942]/50 p-1 rounded-lg">
              <TabsTrigger value="filters" className="data-[state=active]:bg-[#0F2942] rounded-md transition-colors">
                Filters
              </TabsTrigger>
              <TabsTrigger value="sort" className="data-[state=active]:bg-[#0F2942] rounded-md transition-colors">
                Sort
              </TabsTrigger>
            </TabsList>

            <TabsContent value="filters" className="mt-4">
              <ScrollArea className="h-[60vh] pr-4">
                <AdvancedFilters searchType={searchType} />
              </ScrollArea>
            </TabsContent>

            <TabsContent value="sort" className="mt-4">
              <ScrollArea className="h-[60vh] pr-4">
                <SortOptions searchType={searchType} />
              </ScrollArea>
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    </div>
  )
}

function BooleanFilterSelect({
  label,
  value,
  onChange,
}: {
  label: string
  value: BooleanFilter
  onChange: (value: BooleanFilter) => void
}) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <Select
        value={value === null ? "unset" : value.toString()}
        onValueChange={(v) => {
          if (v === "unset") onChange(null)
          else onChange(v === "true")
        }}
      >
        <SelectTrigger className="bg-[#0F2942]/80 border-white/10">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="unset">Any</SelectItem>
          <SelectItem value="true">Yes</SelectItem>
          <SelectItem value="false">No</SelectItem>
        </SelectContent>
      </Select>
    </div>
  )
}

function AdvancedFilters({ searchType }: { searchType: string }) {
  const [hasDescription, setHasDescription] = React.useState<BooleanFilter>(null)
  const [hasScreenshot, setHasScreenshot] = React.useState<BooleanFilter>(null)
  const [isOfficial, setIsOfficial] = React.useState<BooleanFilter>(null)
  const [hasEro, setHasEro] = React.useState<BooleanFilter>(null)

  return (
    <div className="space-y-6">
      {searchType === "vn" && (
        <>
          <div className="space-y-2">
            <Label htmlFor="lang">Language</Label>
            <Input id="lang" placeholder="e.g. en,ja" className="bg-[#0F2942]/80 border-white/10" />
            <p className="text-sm text-white/60">Separate multiple values with commas</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="platform">Platform</Label>
            <Input id="platform" placeholder="e.g. win,lin,mac" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="length">Length (hours)</Label>
            <Input id="length" type="number" placeholder="e.g. 10" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="released">Release Date</Label>
            <Input id="released" placeholder="YYYY-MM-DD" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <BooleanFilterSelect label="Has Description" value={hasDescription} onChange={setHasDescription} />

          <BooleanFilterSelect label="Has Screenshots" value={hasScreenshot} onChange={setHasScreenshot} />
        </>
      )}

      {searchType === "release" && (
        <>
          <div className="space-y-2">
            <Label htmlFor="lang">Language</Label>
            <Input id="lang" placeholder="e.g. en,ja" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="platform">Platform</Label>
            <Input id="platform" placeholder="e.g. win,lin,mac" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="minage">Minimum Age</Label>
            <Input id="minage" type="number" placeholder="e.g. 18" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <BooleanFilterSelect label="Official Release" value={isOfficial} onChange={setIsOfficial} />

          <BooleanFilterSelect label="Has Adult Content" value={hasEro} onChange={setHasEro} />
        </>
      )}

      {searchType === "character" && (
        <>
          <div className="space-y-2">
            <Label htmlFor="gender">Gender</Label>
            <Select>
              <SelectTrigger className="bg-[#0F2942]/80 border-white/10">
                <SelectValue placeholder="Select gender" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="m">Male</SelectItem>
                <SelectItem value="f">Female</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="age">Age</Label>
            <Input id="age" type="number" placeholder="e.g. 18" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="height">Height (cm)</Label>
            <Input id="height" type="number" placeholder="e.g. 170" className="bg-[#0F2942]/80 border-white/10" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="birthday">Birthday (MM-DD)</Label>
            <Input id="birthday" placeholder="e.g. 01-01" className="bg-[#0F2942]/80 border-white/10" />
          </div>
        </>
      )}

      {/* Add other searchType filters */}
    </div>
  )
}

function SortOptions({ searchType }: { searchType: string }) {
  return (
    <div className="space-y-4">
      <Label>Sort By</Label>
      <RadioGroup defaultValue="title">
        {searchType === "vn" && (
          <>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="title" id="title" />
              <Label htmlFor="title">Title</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="released" id="released" />
              <Label htmlFor="released">Release Date</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="rating" id="rating" />
              <Label htmlFor="rating">Rating</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="votecount" id="votecount" />
              <Label htmlFor="votecount">Popularity</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="length" id="length" />
              <Label htmlFor="length">Length</Label>
            </div>
          </>
        )}
        {/* Keep other searchType options */}
      </RadioGroup>

      <div className="mt-6">
        <Label>Order</Label>
        <RadioGroup defaultValue="asc" className="mt-2">
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="asc" id="asc" />
            <Label htmlFor="asc">Ascending</Label>
          </div>
          <div className="flex items-center space-x-2">
            <RadioGroupItem value="desc" id="desc" />
            <Label htmlFor="desc">Descending</Label>
          </div>
        </RadioGroup>
      </div>
    </div>
  )
}

