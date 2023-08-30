import re

# expand contractions
RAW_EXPANSION_RULES = """
could've    	could have
he'd 	        he had, he would
he'll 	        he will
he's 	        he has, he is
here's 	        he will
he's    	    how did, how would
how'll      	how will
how're 	        how are
how's 	        how has, how is
I'd 	        I had, I would
I'll     	    I will
I'm  	        I am
I've     	    I have
it'd     	    it had, it would
it'll 	        it will
it's    	    it has, it is
let's 	        let us
might've    	might have
must've     	must have
she'd 	        she had, she would
she'll 	        she will
she's 	        she has, she is
should've 	    should have
somebody's 	    somebody has, somebody is
someone's 	    someone has, someone is
something's 	something has, something is
that'd 	        that would
that'll     	that will
that's 	        that has, that is
there's     	there has, there is
there're    	there are
these'll    	these will
these're    	these are
they'd 	        they had, they would
they'll     	they will
they're     	they are
they've     	they have
this'll     	this will
this's 	        this has, this is
those'll    	those will
we'd 	        we had, we would
we'll   	    we will
we're 	        we are
we've 	        we have
what'd  	    what did
what'll       	what will
what're     	what are
what's   	    what has, what is
what've     	what have
when'd  	    when did
when's  	    when has, when is
where'd     	where did
where'll     	where will
where're     	where are
where's     	where has, where is
where've     	where have
which's     	which has, which is
who'd 	        who did, who had, who would
who'll   	    who will
who're  	    who are
who's 	        who has, who is
who've  	    who have
why'd 	        why did
why're 	        why are
why's 	        why has, why is
would've     	would have
you'd   	    you had, you would
you'll  	    you will
you're  	    you are
you've  	    you have
aren't  	    are not
can't   	    can not
couldn't    	could not
didn't      	did not
doesn't     	does not
don't 	        do not
hadn't 	        had not
hasn't 	        has not
haven't 	    have not
isn't 	        is not
mustn't 	    must not
shouldn't 	    should not
wasn't 	        was not
weren't 	    were not
won't 	        will not
wouldn't 	    would not
"""


class Expander:
    _expansion_rules: dict

    def __init__(self):
        self._expansion_rules = self._load_expansion_rules()

    def _load_expansion_rules(self) -> dict:
        expansion_rules_pairs = re.findall(
            r"([\w]*\'[\w]*)\s+(.*)", RAW_EXPANSION_RULES
        )
        return dict(
            [
                (contracted, re.findall(r"[\w]+\s+[\w]+", expanded)[0])
                for contracted, expanded in expansion_rules_pairs
            ]
        )

    def expand_contractions(self, raw_text) -> str:
        rules = self._expansion_rules
        expanded_text = raw_text
        for contraction in rules:
            expansion = rules[contraction]
            expanded_text = re.sub(
                contraction, expansion, expanded_text, flags=re.IGNORECASE
            )
        return expanded_text
