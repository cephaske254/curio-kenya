from .views import social_links
from decouple import config


def global_context(request):
    return {
        'paypal_client_id': config('PAYPAL_CLIENT_ID'),
        'social_links': social_links,
        'no_item_found': '''
               <div class="col-md-8 col-lg-6 col-sm-12 mx-auto d-flex flex-column justify-content-center" style="height:70vh">
            <div class="card border-0 shadow d-flex flex-column align-items-center bg-dark-light">
                <div class="card-body">
                    <p class="h1" style="font-size: 30pt;">WHOOPS!</p>
                    <p class="my-0 mx-3 text-center">NO ITEM FOUND</p>
                </div>
                <div class="d-flex w-100 py-2">
                    <a href="../" class="btn btn-sm btn-dark col mx-2">
                        <i class="fas fa-arrow-circle-left"></i> GO BACK
                    </a>
                    <a href="/shop" class="btn btn-sm btn-dark col mx-2">
                        TO SHOP <i class="fas fa-shopping-cart"></i>
                    </a>
                </div>
            </div>
        </div>
        '''
    }
