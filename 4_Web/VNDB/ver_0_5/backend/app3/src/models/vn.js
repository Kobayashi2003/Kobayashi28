const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const VN = sequelize.define('VN', {
    id: {
        type: DataTypes.STRING(255),
        primaryKey: true
    },
    title: DataTypes.STRING(255),
    alttitle: DataTypes.STRING(255),
    titles: DataTypes.JSONB,
    aliases: DataTypes.ARRAY(DataTypes.STRING),
    olang: DataTypes.STRING(10),
    devstatus: DataTypes.INTEGER,
    released: DataTypes.ARRAY(DataTypes.INTEGER),
    languages: DataTypes.ARRAY(DataTypes.STRING),
    platforms: DataTypes.ARRAY(DataTypes.STRING),
    image: DataTypes.JSONB,
    length: DataTypes.INTEGER,
    length_minutes: DataTypes.INTEGER,
    length_votes: DataTypes.INTEGER,
    description: DataTypes.TEXT,
    screenshots: DataTypes.ARRAY(DataTypes.JSONB),
    relations: DataTypes.ARRAY(DataTypes.JSONB),
    tags: DataTypes.ARRAY(DataTypes.JSONB),
    developers: DataTypes.ARRAY(DataTypes.JSONB),
    editions: DataTypes.ARRAY(DataTypes.JSONB),
    staff: DataTypes.ARRAY(DataTypes.JSONB),
    va: DataTypes.ARRAY(DataTypes.JSONB),
    extlinks: DataTypes.ARRAY(DataTypes.JSONB),
    characters: DataTypes.ARRAY(DataTypes.JSONB),
    releases: DataTypes.ARRAY(DataTypes.JSONB)
}, {
    tableName: 'vn',
    timestamps: false,
    hooks: {
        beforeValidate: () => { throw new Error('VN model is read-only'); },
        afterValidate: () => { throw new Error('VN model is read-only'); },
        beforeCreate: () => { throw new Error('VN model is read-only'); },
        afterCreate: () => { throw new Error('VN model is read-only'); },
        beforeDestroy: () => { throw new Error('VN model is read-only'); },
        beforeDelete: () => { throw new Error('VN model is read-only'); },
        afterDestroy: () => { throw new Error('VN model is read-only'); },
        afterDelete: () => { throw new Error('VN model is read-only'); },
        beforeUpdate: () => { throw new Error('VN model is read-only'); },
        afterUpdate: () => { throw new Error('VN model is read-only'); },
        beforeSave: () => { throw new Error('VN model is read-only'); },
        afterSave: () => { throw new Error('VN model is read-only'); },
        beforeBulkCreate: () => { throw new Error('VN model is read-only'); },
        afterBulkCreate: () => { throw new Error('VN model is read-only'); },
        beforeBulkDestroy: () => { throw new Error('VN model is read-only'); },
        beforeBulkDelete: () => { throw new Error('VN model is read-only'); },
        afterBulkDestroy: () => { throw new Error('VN model is read-only'); },
        afterBulkDelete: () => { throw new Error('VN model is read-only'); },
        beforeBulkUpdate: () => { throw new Error('VN model is read-only'); },
        afterBulkUpdate: () => { throw new Error('VN model is read-only'); }
    }
});

VN.create = VN.update = VN.destroy = VN.upsert = VN.truncate = () => {
    throw new Error('VN model is read-only');
};

VN.bulkCreate = VN.bulkUpdate = VN.bulkDestroy = () => {
    throw new Error('VN model is read-only');
};

module.exports = VN;