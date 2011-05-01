$a=0
def inc()
	$a+=1
end
#monkey patch - string class
class String
  def rotate_left(n=1)
    n=1 unless n.kind_of? Integer
    n.times do
      char = self.shift
      self.push(char)
    end
    self
  end
  def push(other)
    newself = self + other.to_s.dup.shift.to_s
    self.replace(newself)
  end
  def shift
    return nil if self.empty?
    item=self[0]
    self.sub!(/^./,"")
    return nil if item.nil?
    item.chr
  end
  def rotate_right(n=1)
    n=1 unless n.kind_of? Integer
    n.times do
      char = self.pop
      self.unshift(char)
    end
    self
  end
  def pop
    return nil if self.empty?
    item=self[-1]
    self.chop!
    return nil if item.nil?
    item.chr
  end
  def unshift(other)
    newself = other.to_s.dup.pop.to_s + self
    self.replace(newself)
  end  
end

#initialize costs matrix as bidimensional hash
def initialize_costs_matrix(file=nil)
	a={}
	if file==nil
		a['A']={}
		a['C']={}
		a['G']={}
		a['T']={}
		a['-']={}
		
		a['A']['A']=0
		a['A']['C']=1
		a['A']['G']=1
		a['A']['T']=1
		a['A']['-']=0
		
		a['C']['A']=a['A']['C']
		a['C']['C']=0
		a['C']['G']=1
		a['C']['T']=1
		a['C']['-']=0
		
		a['G']['A']=a['A']['G']
		a['G']['C']=a['C']['G']
		a['G']['G']=0
		a['G']['T']=1
		a['G']['-']=0
		
		a['T']['A']=a['A']['T']
		a['T']['C']=a['C']['T']
		a['T']['G']=a['G']['T']
		a['T']['T']=0
		a['T']['-']=0
		
		a['-']['A']=a['A']['-']
		a['-']['C']=a['C']['-']
		a['-']['G']=a['G']['-']
		a['-']['T']=a['T']['-']
		a['-']['-']=0
	else
		#initialize from file
	end
	return a
end
#min string length
a=10
#max string length
b=30
#number of random strings
n=2

# Generates a random string from a set of easily readable characters
def generate_random_string(min=10,max=30)
  size=min+rand(max-min)
  charset = %w{A C G T}
  (0...size).map{ charset.to_a[rand(charset.size)] }.join
end

# Alignment function
def align_strings(s1,s2)
  #swap strings so s2 is shorter than s1
  if s1.length<s2.length
    t=s2
	s2=s1
	s1=t
  end
  #s1 string length
  ls1=s1.length
  #s2 string length
  ls2=s2.length
  #s1+s2 string total length
  length=ls1+ls2

  #ns1: ----XXXXXXXXXXXXXXXXXXX----
  #ns2: YYYY-----------------------
  ns1=right_gaps_padding(left_gaps_padding(s1,ls2),ls2) #put gaps on the left and right of longer string
  ns2=right_gaps_padding(s2,length) #put gaps on the right of shorter string
  
  [ns1,ns2]
end

#put gaps on the left of longer string
def left_gaps_padding(s,l)
  p=''
  l.times{p<<'-'}
  p+s
end
#put gaps on the right of shorter string
def right_gaps_padding(s,l)
  p=''
  l.times{p<<'-'}
  s+p
end

def rotate_strings(s1,s2)
	alignments=[]
	ns1,ns2=align_strings(s1,s2)
	((s1+s2).length+1).times do
	  #puts ns1,ns2
	  alignment = character_matching(ns1,ns2) #returns nil or an hash {:s1=>"...",:s2=>"...",:matches=>"..."}
	  alignments.push alignment unless alignment.nil?
	  ns2.rotate_right
	end
	alignments
end

#find how many character matches
def character_matching(s1,s2)
    matching=0
	s1.length.times do |i|
		matching+=1 if s1[i]==s2[i] and s1[i]!="-"
	end
	if matching > 0
		return {:s1=>s1.clone,:s2=>s2.clone,:matching=>matching}
	else
		return {:s1=>s1.clone,:s2=>s2.clone,:matching=>0}
	end
end

def substitution_cost(s1,s2,costs)
	cost=0
	s1.length.times do |i|
		cost+=costs[s1[i..i]][s2[i..i]] if s1[i]!=s2[i]
	end
	##puts s1,s2,cost
	cost
end

def split_sequences_by_longest_match(s1,s2)
	return nil
end
def find_matches(s1,s2)
	matching=[]
	if s2.length==s1.length
		s1.length.times do |i|
			if s1[i]==s2[i]
				matching.push(s1[i])
			else
				matching.push('-')
			end
		end
	end
	return matching.join
end
def remove_duplicated_gaps_from_beginning_and_ending(s1,s2)
	ns1=[]
	ns2=[]
	if s2.length==s1.length
		s1.length.times do |i|
			unless s1[i]==s2[i] and s2[i]=='-'
				ns1.push(s1[i])
				ns2.push(s2[i])
			end
		end
	end
	return ns1.join,ns2.join
end

def find_min_cost_alignment(alignments,costs)
	bestalignment={}
	#initialize bestalignment and mincost with first cost
	bestalignment[:s1],bestalignment[:s2]=alignments.first[:s1],alignments.first[:s2]
	mincost=substitution_cost(bestalignment[:s1],bestalignment[:s2],costs)

	#cerca l'allineamento a costo minimo fra tutti i possibili
	alignments.each do |a|
		cost=substitution_cost(a[:s1],a[:s2],costs)
		if cost<mincost
			bestalignment=a.clone
			mincost=cost
		end
	end
	bestalignment[:s1],bestalignment[:s2] = remove_duplicated_gaps_from_beginning_and_ending(bestalignment[:s1],bestalignment[:s2])
	return bestalignment
end

def sequence_alignment(s1,s2)
inc
	puts "\nNew recursive call on sequences:",s1,s2
	#initialize costs matrix as bidimensional hash
	costs = initialize_costs_matrix

	#ruota le stringhe e produce tutti i possibili allineamenti
	# --aa  -aa  aa  aa- 
	# aa--  aa-  aa  -aa
	alignments=rotate_strings(s1,s2)
	#bestalignment conterrà.. indovina un po?
	bestalignment=nil
	#puts alignments.inspect
	if alignments.length>0
		bestalignment = find_min_cost_alignment(alignments,costs)

		#puts "\nMin cost matching"
		#puts bestalignment[:s1]
		#puts bestalignment[:s2],"\n"
		
		matches = find_matches(bestalignment[:s1],bestalignment[:s2])
		match = matches.split('-').map{|e|
			if e == ''
				nil
			else
				e
			end
		}.compact.sort_by{|e|
			e.length
		}.last
		
		unless match.nil?
			#Split della stringa in corrispondenza di matches
			puts "\nNext split on: #{match}"
			startindex=matches.index(match)
			endindex=matches.index(match)+match.length-1
			puts "Starts form char at position #{startindex} to #{endindex}"
			
			if startindex>0
				puts "\nLeft part:"
				puts ns1=bestalignment[:s1][0..startindex-1]
				puts ns2=bestalignment[:s2][0..startindex-1]
			else
				ns1=""
				ns2=""
			end
			
			if endindex<bestalignment[:s1].length-1
				puts "\nRight part:"
				puts ns3=bestalignment[:s1][endindex+1..-1]
				puts ns4=bestalignment[:s2][endindex+1..-1]
			else
				ns3=""
				ns4=""
			end
			
			#Gestione delle chiamate ricorsive per le sottostringhe di sinistra
			
			ns1,ns2=sequence_alignment(ns1,ns2) if ns1.length>0
			#Gestione delle chiamate ricorsive per le sottostringhe di sinistra
			ns3,ns4=sequence_alignment(ns3,ns4) if ns3.length>0
			#fusione
			s1=ns1+match+ns3
			s2=ns2+match+ns4
			#assegnamento
			s1,s2=bestalignment[:s1],bestalignment[:s2]
		else
			s1,s2=bestalignment[:s1],bestalignment[:s2]
		end
	end
	puts "\n"
	return s1,s2
end


###################################
#                                 #
#DI QUI PARTE IL PROGRAMMAAAAAAAA!#
#                                 #
###################################


#assign and print random ACGT strings
puts s1=generate_random_string(a,b)
puts s2=generate_random_string(a,b)

#di test...
#puts s1="AAACCCATCACACGGGACATATT"
#puts s2="AACCAGTCACACGGCA"

#io mi aspetterei questa... costo=11 (diversità)
#AAACCCA-TCACACGG-GACATATT
#AA-CC-AGTCACACGGC-A------

#AAACCCATCACACGGGACATATT COSTO=10
#-AACCAGTCACACGGCA------

s1,s2 = sequence_alignment(s1,s2)
puts "\n\nBest alignment:"
puts s1,s2

puts "\n\n\n",$a
