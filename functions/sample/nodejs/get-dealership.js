/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    
    // Define the database and selector
    const dbname = params.dbname; // Make sure to pass 'dbname' as a parameter when invoking the action
    // Build selector based on query parameters
    let selector = {};
    if (params.state) {
        selector.state = params.state;
    }

    try {
        // Call getMatchingRecords and await its resolution
        const records = await getMatchingRecords(cloudant, dbname, selector);
        return {body: records};
    } catch (err) {
        // Error handling
        return { error: err.message };
    }
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 async function getMatchingRecords(cloudant,dbname, selector) {
    const result = await cloudant.postFind({db:dbname,selector:selector})
    return {result: result.result.docs}
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 async function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }
