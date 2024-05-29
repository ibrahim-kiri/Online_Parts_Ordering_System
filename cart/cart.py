from store.models import Part

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart

    def add(self, part, quantity):
        part_id = str(part.id)
        part_qty = str(quantity)

        # Logic
        if part_id in self.cart:
            pass
        else:
            # self.cart[part_id] = {'price': str(part.price)}
            self.cart[part_id] = int(part_qty)

        self.session.modified = True

    def cart_total(self):
        # Get part Ids
        part_ids = self.cart.keys()
        # lookup for those keys in our parts database model
        parts = Part.objects.filter(id__in=part_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        
        for key, value in quantities.items():
            # Convert key string into integer so we can do math
            key = int(key)
            for part in parts:
                if part.id == key:
                    if part.is_sale:
                        total = total + (part.sale_price * value)
                    else:
                        total = total + (part.price * value)
        return total

    def __len__(self):
        return len(self.cart)

    def get_pars(self):
        # Get ids from cart
        part_ids = self.cart.keys()
        # Use ids to lookup parts in database model
        parts = Part.objects.filter(id__in=part_ids)

        # Return those looked up parts
        return parts
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, part, quantity):
        part_id = str(part)
        part_qty = int(quantity)

        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[part_id] = part_qty

        self.session.modified = True

        thing = self.cart
        return thing
    
    def delete(self, part):
        part_id = str(part)
        # Delete from dictionary/cart
        if part_id in self.cart:
            del self.cart[part_id]

        self.session.modified = True

    